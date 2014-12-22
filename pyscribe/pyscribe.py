import sys
import ast
import re
import inspect

class Scriber(object):
    def __init__(self):
        self.show_line_num = True
        self.api_calls = [function for function, _ in inspect.getmembers(self, predicate=inspect.ismethod)][1:] # don't want '__init__'
        self.api_calls.append("Scriber")

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

    def gen_desugared(self, line_mapping, program_file, program_ast):
        desugared_copy_name = program_file[:-3] + "_desugared.py"
        desugared_copy = open(desugared_copy_name, 'w')
        program = open(program_file, 'r')

        for line_num, line_content in enumerate(program.readlines()):
            if line_content in line_mapping.values():
                desugared_copy.write(self.desugar_line(line_content[:-1], line_num, program_ast)) # don't want to include \n
            else:
                desugared_copy.write(line_content)

        program.close()
        desugared_copy.close()
        return desugared_copy_name

    def get_variable_id(self, line, program_ast):
        parsed_line = ast.dump(ast.parse(line).body[0])
        for node in ast.walk(program_ast):
            if parsed_line == ast.dump(node):
                return node.value.args[0].id

    def desugar_line(self, line, line_num, program_ast):
        if self.show_line_num:
            desugared_line = "From line " + str(line_num) + ": "
        else:
            desugared_line = ""
        function = [api_call for api_call in self.api_calls if api_call in line]
        assert len(function) == 1 # For now just one function call per line
        if function[0] == "scribe":
            desugared_line += self.scribe(line, program_ast)
        output =  "print('" + desugared_line + ")\n"
        return output

        #print("x is the " + type(x) + " " + x)


    def scribe(self, line, program_ast):
        variable_id = self.get_variable_id(line, program_ast)
        return variable_id + " is the ' + type(" + variable_id + ") + ' ' + str(" + variable_id + ")"

def main():
    scribe = Scriber()
    program_file = sys.argv[1]
    if ".py" != program_file[-3:]:
       raise KeyError("Please pass in a Python file as argument")
    line_mapping = scribe.gen_line_mapping(program_file)
    clean_copy = scribe.gen_clean_copy(program_file, line_mapping)
    program_ast = scribe.gen_ast(program_file)
    desugared_copy = scribe.gen_desugared(line_mapping, program_file, program_ast)

if __name__=="__main__":
    main()

