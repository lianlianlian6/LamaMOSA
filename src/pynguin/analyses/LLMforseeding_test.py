import time
import subprocess
import os

python_executable = "your_interpreter_path"

directory = "your_module_under_test_file_folder_path"
test_directory = "output_test_folder_path"

for root, dirs, files in os.walk(directory):
    # 忽略子目录
    dirs[:] = []

    for file in files:
        if file.endswith(".py"):
            # 获取文件的绝对路径和文件名（不含扩展名）
            module_path = os.path.join(root, file)
            module_name = os.path.splitext(file)[0]
            # 定义 Pynguin 命令
            LLMforseeding_command = [
                python_executable, "your_path\LamaMOSA\src\pynguin/analyses\LLMforseeding.py",
                "--project_path", directory,
                "--module_name", module_name,
                "--output_path", test_directory,
                "--module_path", module_path
            ]
            print(f"Generating initial population for {module_name}")
            # 运行 Pynguin 命令
            result = subprocess.run(LLMforseeding_command)
