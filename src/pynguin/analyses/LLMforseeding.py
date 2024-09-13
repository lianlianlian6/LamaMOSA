import json
import argparse
import sys
import csv
import time
from pynguin.analyses.astforcall import *
from pynguin.cli import main
import openai
from pathlib import Path
import os

openai.api_key = 'your_api'

def gpt35(prompt, model="gpt-4-turbo", temperature=0.7  #gpt-3.5-turbo, gpr-4-turbo, gpt-4o-mini
           ):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a software engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        # max_tokens=max_tokens,
        # top_p=top_p,
        # stop=stop
    )

    message = response["choices"][0]["message"]["content"]
    return message

def get_code_from_module(module_path, encoding='utf-8'):   # 代码
    # 读取module_path中的代码内容
    with open(module_path, 'r', encoding=encoding) as file:
        source_code = file.read()
    return source_code

def get_branches(function_to_test):
    prompt_to_get_branches = f"""
Here is the function to test:{function_to_test}
Please analyze the branches in the code above.
    """
    response = gpt35(prompt_to_get_branches)
    return prompt_to_get_branches, response

def generate_test_cases(module_name, prompt_to_get_branches, branch_response, unit_test_package="pytest"):
    # index = sys.argv.index("--module_name")
    # module_name = sys.argv[index + 1]
    prompt_to_get_test_cases = f"""
According to the analysis above, please write a python test file with {unit_test_package} for it to cover branches as many as possible, and here are some requirements:
- The function to be tested is in the file {module_name}, please directly use "import {module_name}" rather than "from {module_name} import ..."
- Use 'def' instead of 'Class' to generate test cases.
- Do not use @pytest.mark.parametrize.
    """
    final_prompt = prompt_to_get_branches + branch_response + prompt_to_get_test_cases
    response = gpt35(final_prompt)
    return response, final_prompt

def extract_code_from_test_cases(module_name, source_code):
    prompt_to_get_branches, branch_response = get_branches(source_code)
    test_cases, prompt_to_get_test_file = generate_test_cases(module_name, prompt_to_get_branches, branch_response)
    code_start_index = test_cases.find("```python\n") + len("```python\n") - 1
    code_end_index = test_cases.find("```\n", code_start_index)
    code_output = test_cases[code_start_index:code_end_index]
    while True:
        try:
            compile(code_output,'<string>', 'exec')
            break
        except SyntaxError as e:
            lines = code_output.splitlines()
            error_line = e.lineno -1
            del lines[error_line]
            code_output = "\n".join(lines)
    return code_output


def write_code_to_file(code, file_path):
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(code)

        # 返回0表示成功
        return 0
    except Exception as e:
        print(f"写入文件时发生错误: {e}")
        # 返回非0值表示失败
        return 1


def process_module(module_path, module_name):
    # 读取模块代码
    source_code = get_code_from_module(module_path)
    project_path = os.path.dirname(module_path)
    # 创建 initial_population.py 文件路径
    file_name = os.path.basename(module_path)

    # 定义initial_population.py文件的路径
    initial_population_path = os.path.join(project_path, 'ini_test', f'test_{file_name}')
    if not os.path.isdir(os.path.join(project_path, 'ini_test')):
        os.makedirs(os.path.join(project_path, 'ini_test'))
    with open(initial_population_path, 'w') as file:
        pass
    print(f"The file {initial_population_path} has been created.")

    # 提取测试用例中的代码
    code_output = extract_code_from_test_cases(module_name, source_code)

    # 写入文件
    result = write_code_to_file(code_output, initial_population_path)

    return result, initial_population_path



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and transform code based on AST.")
    parser.add_argument("--project_path", type=str, default="", help="")
    parser.add_argument("--module_name", type=str, default="", help="")
    parser.add_argument("--output_path", type=str, default="", help="")
    parser.add_argument("--module_path", type=str, default="", help="")
    args = parser.parse_args()

    start_time = time.time()

    create_file_result, initial_population_path = process_module(args.module_path, args.module_name)

    if create_file_result == 0:
        print("Successfully generated initial test cases!")
        num_cases, num_parsable_cases, ast_parsable_cases = LLM_initial_population(args.module_path, initial_population_path)
        end_time = time.time()
        LLM_time = end_time - start_time
        print(f"运行时间：{LLM_time} 秒")
        # 将变量值写入文件
        file_exists = os.path.exists(
            os.path.join(args.project_path, 'ini_test','LLM_output.csv'))
        with open(
            os.path.join(args.project_path, 'ini_test','LLM_output.csv'),
            mode='a', newline='') as file:
            writer = csv.writer(file)
            # 写入标题行（如果文件不存在）
            if not file_exists:
                writer.writerow(["module_name", "num_cases", "num_parsable_cases", "ast_parsable_cases","LLM_time"])
            writer.writerow([args.module_name, num_cases, num_parsable_cases, ast_parsable_cases, LLM_time])
    else:
        print("Failed to generate unit test cases")
