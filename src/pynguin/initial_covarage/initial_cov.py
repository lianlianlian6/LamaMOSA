from pynguin.ga.algorithms.generationalgorithm import GenerationAlgorithm
from pynguin.generator import _setup_and_check, ReturnCode, _instantiate_test_generation_strategy
import pynguin.configuration as config
from pynguin.initial_covarage.main import main
from pynguin.slicer.statementslicingobserver import StatementSlicingObserver
import argparse
import csv
import sys
import time
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
    print(f"initial_coverage of {args.module_name}:")
    initial_coverage = main(argv)
    print(initial_coverage)
    file_exists = os.path.exists(
        os.path.join(args.project_path, 'ini_test','LLM_initial_cov.csv'))
    with open(
        os.path.join(args.project_path, 'ini_test', 'LLM_initial_cov.csv'),
        mode='a', newline='') as file:
        writer = csv.writer(file)
        # 写入标题行（如果文件不存在）
        if not file_exists:
            writer.writerow(["module_name", "initial_coverage"])
        writer.writerow([args.module_name, initial_coverage])

