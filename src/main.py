import argparse
import csv
import sys
import time
from pynguin.cli import main
import os
from pathlib import Path
import threading
os.environ['PYTHONIOENCODING'] = 'utf-8'

def args_to_argv(args):
    argv = [sys.argv[0]]  # 脚本名称
    for action in parser._actions:
        dest = action.dest
        if dest in vars(args):
            value = getattr(args, dest)
            if value is not None:
                argv.append(f"--{dest}")
                argv.append(str(value))
    return argv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Pygnguin.")
    parser.add_argument("--project_path", type=str, default="", help="")
    parser.add_argument("--module_name", type=str, default="", help="")
    parser.add_argument("--output_path", type=str, default="", help="")
    parser.add_argument("--initial_population_seeding", type=bool, default=True, help="")
    parser.add_argument("--initial_population_data", type=str, default="", help="")
    parser.add_argument("--algorithm", type=str, default="DYNAMOSA", help="")
    parser.add_argument("--coverage-metrics", type=str, default="BRANCH", help="")
    # parser.add_argument("--create-coverage-report", type=bool, default=True, help="")
    args = parser.parse_args()
    argv = args_to_argv(args)
    argv.append('-v')
    run_res, cov_val, generation_time = main(argv)
    file_exists = os.path.exists(
        os.path.join(args.project_path, 'ini_test','LLM_output_cov.csv'))
    with open(
        os.path.join(args.project_path, 'ini_test', 'LLM_output_cov.csv'),
        mode='a', newline='') as file:
        writer = csv.writer(file)
        # 写入标题行（如果文件不存在）
        if not file_exists:
            writer.writerow(["module_name", "Branch_coverage", "DynaMOSA_time"])
        writer.writerow([args.module_name, cov_val, generation_time])

