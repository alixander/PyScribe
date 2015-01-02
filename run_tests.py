#!/usr/bin/env python

import os
import difflib
import time
import subprocess

log = "pyscribe_log.txt"

def run_test(test_path):
    command = "./pyscribe/pyscribe.py " + test_path + "> " + log
    subprocess.call(command, shell=True)

def run_comparison(output, correct):
    diff = difflib.unified_diff(open(output,'U').readlines(),
                                open(correct,'U').readlines())
    failed = False
    for line in diff:
        if len(line) > 0:
            failed = True
            break
    if failed:
        print("Comparison failed")
    else:
        print("Test passed")

tests_directory = "tests" + os.sep
test_modules = os.listdir(tests_directory)
print("\n-----Starting test run-----\n")
for module in test_modules:
    print("Running test module: *" + str(module) + "*\n")
    tests = filter(lambda x: "_desugared" not in x and
                             "_clean" not in x and
                             x.endswith(".py"),
                             os.listdir(tests_directory + module))
    for test in tests:
        start = time.time()
        test_path = tests_directory + module + os.sep

        print("Desugaring and running test file: " + str(test))
        run_test(test_path + test)

        print("Comparing result with correct version")
        correct_file_path = test_path + test[:-3] + "_correct"
        run_comparison(log, correct_file_path)

        print("Test finished in " + str(time.time()-start) + "ms\n")
print("-----Finished running all tests-----\n")
