import sys
import ast
import re
import inspect

class scriber(object):
    def __init__(self):
        self.lineMapping = {}
        self.api_calls = [function for function, _ in inspect.getmembers(self, predicate=inspect.ismethod)][1:] # don't want '__init__'

    def gen_line_mapping(self, program_file):
        program = open(program_file, 'r')
        for line_num, line_content in enumerate(program.readlines()):
            is_api_call = False
            for func in self.api_calls:
                if ("." + func + "(") in line_content:
                    self.lineMapping[line_num+1] = line_content # line num in most text editors is 1-indexed
        program.close()

    def scribe(self, obj):
        pass

def main():
    scribe = scriber()
    scribe.gen_line_mapping(sys.argv[1])

if __name__=="__main__":
    main()

