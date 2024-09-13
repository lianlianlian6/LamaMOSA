import ast
import astor
import pytest
import inspect
import random
import pynguin.ga.testcasechromosome as tcc
import os
from pathlib import Path
import csv
from pynguin.analyses.constants import EmptyConstantProvider
from pynguin.analyses.module import generate_test_cluster
from pynguin.analyses.seeding import AstToTestCaseTransformer
from pynguin.testcase import export

counter = 0  # 全局计数器

def process_initial_population_file(file_path, module_name):   ##判别器
    with open(file_path, 'r', encoding='utf-8') as file:
        source_code = file.read()

    test_cluster = generate_test_cluster(module_name)  ##待测单元
    transformer = AstToTestCaseTransformer(
        test_cluster, False, EmptyConstantProvider()  # noqa: FBT003
    )
    # 解析源代码为 AST
    parsed_ast = ast.parse(source_code)

    # 遍历 AST 中的所有节点并处理 FunctionDef 节点
    nodes_to_remove = []
    removed_functions_code = []
    num_parsable_cases = 0
    num_cases = 0
    for node in parsed_ast.body:
        if isinstance(node, ast.FunctionDef):
            num_cases += 1
            transformer.visit(node)
            if transformer._current_parsable:
                num_parsable_cases += 1
                continue
            else:
                removed_functions_code.append(astor.to_source(node))
                nodes_to_remove.append(node)

    # 从 AST 中删除需要删除的节点
    for node in nodes_to_remove:
        parsed_ast.body.remove(node)

    # 将修改后的 AST 转换回源代码
    modified_source_code = astor.to_source(parsed_ast)

    # 将修改后的源代码写回 initial_population.py
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_source_code)

    return removed_functions_code, num_parsable_cases, num_cases

def code_parsable(code,module_name):   ##判别器
    test_cluster = generate_test_cluster(module_name)  ##待测单元
    transformer = AstToTestCaseTransformer(
        test_cluster, False, EmptyConstantProvider()  # noqa: FBT003
    )
    # 解析源代码为 AST
    parsed_ast = ast.parse(code)
    transformer.visit(parsed_ast)
    if transformer._current_parsable:
        return 1
    else:
        return 0

# 解决函数调用嵌套
def create_temp_var_name():
    global counter
    temp_var_name = f"_temp_var_{counter}"
    counter += 1
    return temp_var_name

def transform_call_node_nest(call_node):
    new_assignments = []
    new_args = []
    for arg in call_node.args:
        if isinstance(arg, ast.Call) :
            temp_var_name = create_temp_var_name()
            temp_assignment = ast.Assign(
                targets=[ast.Name(id=temp_var_name, ctx=ast.Store())],
                value=arg
            )
            new_assignments.append(temp_assignment)
            new_args.append(ast.Name(id=temp_var_name, ctx=ast.Load()))
            try:
                arg.func.attr
                # Recursively transform nested calls
                nested_assignments = transform_call_node_nest(arg)
                new_assignments.extend(nested_assignments)
            except AttributeError as e:
                pass
        else:
            new_args.append(arg)

    call_node.args = new_args
    return new_assignments

def transform_function_def_nest(func_def):
    new_body = []
    for stmt in func_def.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
            try:
                stmt.value.func.attr    ##遇到外部函数就拆
                assignments = transform_call_node_nest(stmt.value)
                new_body.extend(assignments)
            except AttributeError as e:
                assignments = stmt.value   ##遇到内置函数就保持不变
        new_body.append(stmt)
    func_def.body = new_body
    return func_def

def transform_code_nest(code):
    global counter
    counter = 0  # 重置计数器
    tree = ast.parse(code)
    new_body = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            new_body.append(transform_function_def_nest(node))
        else:
            new_body.append(node)

    tree.body = new_body
    ast.fix_missing_locations(tree)
    new_code = astor.to_source(tree)
    return new_code

# 解决call.args中没有Name属性，调用时参数为常数 b = np.array([1,2,3])
# 解决call.keywords中没有Name属性，调用时参数为常数 b = np.array(a,b=[1,2,3])
def transform_call_node(call_node):
    new_assignments = []
    new_args = []
    for arg in call_node.args:
        if not isinstance(arg, ast.Name):
            temp_var_name = create_temp_var_name()
            temp_assignment = ast.Assign(
                targets=[ast.Name(id=temp_var_name, ctx=ast.Store())],
                value=arg
            )
            new_assignments.append(temp_assignment)
            new_args.append(ast.Name(id=temp_var_name, ctx=ast.Load()))
        else:
            new_args.append(arg)
    call_node.args = new_args

    for keyword in call_node.keywords:
        if not isinstance(keyword.value, ast.Name):
            temp_var_name = create_temp_var_name()
            temp_assignment = ast.Assign(
                targets=[ast.Name(id=temp_var_name, ctx=ast.Store())],
                value=keyword.value
            )
            new_assignments.append(temp_assignment)
            keyword.value = ast.Name(id=temp_var_name, ctx=ast.Store())
    return new_assignments

def transform_function_def(func_def):
    new_body = []
    for stmt in func_def.body:
        if isinstance(stmt, (ast.Assign, ast.Expr)) and isinstance(stmt.value, ast.Call):
            assignments = transform_call_node(stmt.value)
            new_body.extend(assignments)
        new_body.append(stmt)
    func_def.body = new_body
    return func_def

def transform_code_value(code):
    global counter
    counter = 0  # 重置计数器
    tree = ast.parse(code)
    new_body = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            new_body.append(transform_function_def(node))
        else:
            new_body.append(node)

    tree.body = new_body
    ast.fix_missing_locations(tree)
    new_code = astor.to_source(tree)
    return new_code

###解决函数调用
builtin_functions = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable',
    'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dir', 'divmod', 'enumerate',
    'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
    'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
    'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
    'print', 'property', 'range', 'repr', 'reversed', 'round', 'setattr', 'slice', 'sorted',
    'staticmethod', 'str', 'sum', 'super', 'type', 'vars', 'zip', '__import__','list', 'set', 'dict', 'tuple'
}   ##不删除那四个

def is_builtin_func_call(call_node):
    """
    判断一个ast.Call节点是否调用的是内置函数
    """
    if not isinstance(call_node, ast.Call):
        return False

    func = call_node.func
    if isinstance(func, ast.Name) and func.id in builtin_functions:
        return True
    return False


def evaluate_builtin_call(call_node):
    """
    评估内置函数调用并返回结果
    """
    func_name = call_node.func.id
    # 评估内置函数调用
    if func_name in builtin_functions:
        value_str =ast.unparse(call_node)
        try:
            eval(f'{value_str}')
            return eval(f'{value_str}')
        except:
            pass
    return None

def transform_code_import(new_source_code):
    tree = ast.parse(new_source_code)
    new_body = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for stmt in node.body:
                if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                    call_node = stmt.value
                    if is_builtin_func_call(call_node):
                        # 将右侧的赋值语句直接改为调用这些内置函数输出的结果
                        res_value = evaluate_builtin_call(stmt.value)
                        if res_value is not None:
                            stmt.value = ast.Constant(value=res_value)
                    # elif isinstance(call_node.func, ast.Attribute):
                    #     random_value = handle_module_function_call(call_node.func, project_path)
                    #     if random_value is not None:
                    #         stmt.value = ast.parse(random_value).body[0].value
            new_body.append(node)
        else:
            new_body.append(node)

    tree.body = new_body
    ast.fix_missing_locations(tree)
    new_code = astor.to_source(tree)
    return new_code

def append_code_to_file(file_path, new_source_code):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write('\n')  # 添加换行符，以确保新代码与现有代码分开
            file.write(new_source_code)
        return 0
    except Exception as e:
        print(f"Failed to append code to {file_path}: {e}")
        return -1


def LLM_initial_population(module_path, initial_population_path):
    path = Path(module_path)
    module_name = path.stem
    removed_functions_code, num_parsable_cases, num_cases = process_initial_population_file(initial_population_path,
                                                                                            module_name)
    ast_parsable_cases = 0
    for code in removed_functions_code:
        # print(f"Removed function code:\n{code}")
        transformed_code = transform_code_nest(code)
        # print(f"transformed_code:\n{transformed_code}")
        edited_code = transform_code_import(transformed_code)
        # print(f"edited_code:\n{edited_code}")
        new_source_code = transform_code_value(edited_code)
        # print(f"new_source_code:\n{new_source_code}")
        parseAST_result = append_code_to_file(initial_population_path, new_source_code)
        ast_parsable_cases += code_parsable(new_source_code, module_name)

    return  num_cases, num_parsable_cases, ast_parsable_cases
