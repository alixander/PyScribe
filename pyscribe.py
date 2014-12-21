import sys
import ast
import re
import inspect

class scriber(object):
    def __init__(self):
        self.api_calls = [function for function, _ in inspect.getmembers(self, predicate=inspect.ismethod)][1:] # don't want '__init__'
        self.api_calls.append("scriber")
        self.clean_copy_file = ""
        self.AST = ""

    def gen_line_mapping(self, program_file):
        line_mapping = {}
        program = open(program_file, 'r')
        for line_num, line_content in enumerate(program.readlines()):
            is_api_call = False
            for func in self.api_calls:
                if ("." + func + "(") in line_content:
                    line_mapping[line_num+1] = line_content # line num in most text editors is 1-indexed
        program.close()
        return line_mapping

    def gen_clean_copy(self, program_file, line_mapping):
        program = open(program_file, 'r')
        clean_copy_name = program_file[:-3] + "_clean.py"
        clean_copy = open(clean_copy_name, 'w')
        for line_num, line_content in enumerate(program.readlines()):
            if (line_num + 1) not in line_mapping.keys():
               clean_copy.write(line_content)
        clean_copy.close()
        program.close()
        return clean_copy_name

    def gen_ast(self, program_file):
        f = open(program_file, 'r')
        ast_output = ast.parse(f.read())
        f.close()
        return ast_output

    def scribe(self, obj):
        pass

def main():
    scribe = scriber()
    program_file = sys.argv[1]
    if ".py" != program_file[-3:]:
       raise KeyError("Please pass in a Python file as argument")
    line_mapping = scribe.gen_line_mapping(program_file)
    clean_copy = scribe.gen_clean_copy(program_file, line_mapping)
    clean_ast = scribe.gen_ast(clean_copy)

if __name__=="__main__":
    main()

