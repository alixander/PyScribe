#!/usr/bin/env python
# encoding: utf-8
"""
pyscribe.py

Copyright (c) 2014 Alexander Wang

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import ast
import re
import inspect

sys.path.append('.')
import utils

class Scriber(object):
    def __init__(self):
        self.show_line_num = True
        self.save_logs = True
        self.api_calls = ['p', 'Scriber']

    def gen_line_mapping(self, program_file):
        """Return a dictionary of lines as keys and the corresponding api call lines as values"""
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
        """Generate and return a clean copy of the file with all references of pyscriber removed"""
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
        #print ast.dump(ast_output)
        return ast_output

    def gen_desugared(self, line_mapping, program_file, program_ast):
        """Generate a desugared version that Python understands from one with PyScriber API calls"""
        desugared_copy_name = program_file[:-3] + "_desugared.py"
        desugared_copy = open(desugared_copy_name, 'w')
        desugared_copy.write("import re\n") #Will be making some regex calls
        program = open(program_file, 'r')

        for line_num, line_content in enumerate(program.readlines()):
            if "Scriber()" in line_content:
                if self.save_logs:
                    indentation = utils.get_indentation(line_content)
                    desugared_copy.write(indentation + "pyscribe_log = open('pyscribe_logs.txt', 'w')\n") # Maybe append?
            elif line_content in line_mapping.values():
                desugared_copy.write(self.desugar_line(line_content[:-1], line_num, program_ast)) # don't want to include \n
            else:
                desugared_copy.write(line_content)

        program.close()
        desugared_copy.close()
        return desugared_copy_name

    def get_variable_id(self, line, program_ast):
        """Return the variable id by finding the line in the program AST and gettings its argument"""
        parsed_line = ast.dump(ast.parse(line).body[0])
        for node in ast.walk(program_ast):
            if parsed_line == ast.dump(node):
                return node.value.args[0].id
        raise KeyError("Was not able to find variable ID")

    def desugar_line(self, line, line_num, program_ast):
        indentation = utils.get_indentation(line)
        line = line[len(indentation):]
        if self.show_line_num:
            desugared_line = "From line " + str(line_num) + ": "
        else:
            desugared_line = ""
        function = [api_call for api_call in self.api_calls if ("." + api_call) in line]
        assert len(function) == 1 # For now just one function call per line
        if function[0] == "p":
            desugared_line += self.scribe(line, program_ast)

        if self.save_logs:
            action = "pyscribe_log.write('"
            ending = "+ '\\n')\n"
        else:
            action = "print('"
            ending = ")\n"
        output =  action + desugared_line + ending

        if len(indentation) > 0:
            output = indentation + output
        return output

    def scribe(self, line, program_ast):
        """The internal method called for basic printing of identifer, type, and value"""
        variable_id = self.get_variable_id(line, program_ast)
        variable_type = "re.search(r\'\\\'[a-zA-Z]*\\\'\', str(type(" + variable_id + "))).group()[1:-1]"
        return variable_id + " is the ' + " + variable_type + " + ' ' + str(" + variable_id + ")"

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

