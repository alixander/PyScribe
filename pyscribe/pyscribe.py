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

import argparse
import uuid
import random
import string
import sys
import os
import ast
import re
import inspect
import subprocess

sys.path.append('.')
import utils

class Scriber(object):
    def __init__(self, filtered=[]):
        pass

    def p(self, obj):
        pass

    def watch(self, obj):
        pass

    def iterscribe(self, obj):
        pass

    def d(self, obj, unit="-"):
        pass

    def save_logs(self, save):
        pass

    def props(self):
        pass


class Watcher(object):
    def __init__(self):
        self.watching = []
        self.watch_lines = {}

    def watch_var(self, var):
        self.watching.append(var)

    def num_watched(self):
        return len(self.watching)

    def set_lines(self, var, lines):
        self.watch_lines[var] = lines

    def new_line_nums(self):
        return sum(self.watch_lines.values(), [])

    def vars_and_lines(self):
        return self.watch_lines.items()


class Runner(object):
    CLEAN_SUFFIX = "_clean.py"

    def __init__(self, logging, no_lines):
        self.show_lines = not no_lines
        self.save_logs = logging

        self.initialized = False
        # p for print, d for distinguish
        self.api_calls = ['p', 'watch', 'iterscribe', 'd', 'Scriber']
        self.imports = ['re', 'pprint', 'datetime']
        self.desugared_lines = []
        self.filtered_labels = []
        self.watcher = Watcher()
        self.shebang = False

    def gen_line_mapping(self, program_file):
        """Return a dictionary of lines as keys and
        the corresponding api call lines as values
        """
        line_mapping = {}
        with open(program_file, 'r') as program:
            for line_num, line_content in enumerate(program.readlines()):
                for func in self.api_calls:
                    if utils.is_ps_call(func, line_content):
                        # line num in most text editors is 1-indexed
                        line_mapping[line_num+1] = line_content
        return line_mapping

    def gen_clean_copy(self, program_file, line_mapping):
        """Generate and return a clean copy of the file
        with all references of pyscriber removed
        """
        with open(program_file, 'r') as program:
            clean_copy_name = program_file[:-3] + self.CLEAN_SUFFIX
            with open(clean_copy_name, 'w') as clean_copy:
                for line_num, line_content in enumerate(program.readlines()):
                    if (line_num + 1) not in line_mapping.keys():
                        clean_copy.write(line_content)
        return clean_copy_name

    def gen_ast(self, program_file):
        with open(program_file, 'r') as f:
            ast_output = ast.parse(f.read())
        return ast_output

    def write_imports(self):
        for imp in self.imports:
            self.desugared_lines.append("import " + imp + "\n")

    def gen_desugared(self, line_mapping, program_file, program_ast):
        """Generate a desugared version that Python understands
        from one with PyScriber API calls
        """
        desugared_copy_name = program_file[:-3] + "_desugared.py"
        with  open(desugared_copy_name, 'w') as desugared_copy:
            with open(program_file, 'r') as program:
                first_call_indentation = ""
                # Check if .close() has been added due to indentation decrease.
                # If not, add it at the end.
                closing_line_added = False

                for line_num, line_content in enumerate(program.readlines()):
                    if line_num == 0:
                        if utils.is_shebang(line_content):
                            self.desugared_lines.append(line_content)
                            self.shebang = True
                        self.write_imports()
                    if re.match(r'(\s)*#', line_content):  # Ignore commented out lines
                        continue
                    indentation = utils.get_indentation(line_content)
                    if (not closing_line_added and
                            self.save_logs and
                            self.initialized and
                            first_call_indentation != "" and
                            len(line_content) > 2 and
                            len(indentation) < len(first_call_indentation)):
                        closing_line = (utils.get_end(first_call_indentation) +
                                        first_call_indentation +
                                        "pyscribe_log.close()\n")
                        closing_line_added = True
                        self.desugared_lines.append(closing_line)
                    if "pyscribe" in line_content:
                        if self.save_logs and "Scriber(" in line_content:
                            self.initialized = True
                            timestamp = utils.get_timestamp(indentation)
                            desugared_line = (indentation +
                                             "pyscribe_log = open('pyscribe_logs.txt', 'w')\n")
                            self.desugared_lines.append(desugared_line + timestamp)
                            first_call_indentation = indentation
                        if "Scriber(" in line_content:
                            self.filtered_labels = utils.get_filtered_labels(line_content, program_ast)
                        self.desugared_lines.append('#' + line_content)
                    elif line_content in line_mapping.values():  # Line matches an API call
                        desugared_line = self.desugar_line(line_content[:-1],
                                                           line_num,
                                                           program_file,
                                                           program_ast)  # don't want to include \n
                        if desugared_line:
                            self.desugared_lines.append(desugared_line)
                    elif (self.watcher.num_watched() > 0 and  # Line matches watched variable change
                          line_num in self.watcher.new_line_nums()):
                        self.desugared_lines.append(line_content)
                        for var, lines in self.watcher.vars_and_lines():
                            if line_num in lines:
                                self.desugared_lines.append(self.variable_change(var,
                                                                                 line_num,
                                                                                 indentation))
                                break  # Should only be true once
                    else:
                        self.desugared_lines.append(line_content)
                if not closing_line_added and self.save_logs and self.initialized:
                    self.desugared_lines.append(utils.get_end('') + "pyscribe_log.close()\n")
            for line in self.desugared_lines:
                desugared_copy.write(line)
        return desugared_copy_name

    def from_line(self, line_num):
        if self.show_lines:
            return "From line " + str(line_num+1) + ": "
        return ""

    def action_and_ending(self, line_num):
        if self.save_logs:
            action = "pyscribe_log.write('"
            ending = "+ '\\n')\n"
        else:
            action = "print('"
            ending = ")\n"
        return action, ending

    def desugar_line(self, line, line_num, program_file, program_ast):
        indentation = utils.get_indentation(line)
        line = line[len(indentation):]
        function = [api_call for api_call in self.api_calls
                    if ("." + api_call) in line]

        assert len(function) == 1  # For now just one function call per line
        if function[0] == "p":
            desugared_line = self.scribe(line, program_ast)
        elif function[0] == "watch":
            desugared_line = self.watch(line, line_num, program_file, program_ast)
        elif function[0] == "iterscribe":
            desugared_line = self.iterscribe(line, line_num, indentation, program_ast)
        elif function[0] == "d":
            desugared_line = self.distinguish(line, program_ast)
        else:
            desugared_line = ""

        if not desugared_line:
            return ""

        action, ending = self.action_and_ending(line_num)
        if self.show_lines:
            output = action + self.from_line(line_num) + desugared_line + ending
        else:
            output = action + desugared_line + ending

        if len(indentation) > 0:
            output = indentation + output
        return output

    def distinguish(self, line, program_ast):
        unit = utils.get_distinguish_unit(line, program_ast)
        return ("\\n" +
                utils.draw_line(unit=unit) +
                self.scribe(line, program_ast) +
                " + '\\n" +
                utils.draw_line(unit=unit) +
                "'")

    def iter_start(self, node, line, line_num, program_ast, indentation):
        action, ending = self.action_and_ending(line_num)
        text = ("' + '" +
                self.scribe(line, program_ast) +
                " + ' at beginning of for loop at line " +
                str(node.lineno) +
                "' ")
        return (indentation[:-4] +
                action +
                utils.draw_line() +
                text +
                ending)

    def offset(self):
        offset = len(self.imports) - 1
        if self.save_logs:
            offset += 1
        return offset

    def iterscribe(self, line, line_num, indentation, program_ast):
        variable_id, variable_type = utils.get_id_and_type(line, program_ast)
        for node in ast.walk(program_ast):
            # TODO: handle nested for loops
            if ('iter' in node._fields and
                ast.dump(ast.parse(line).body[0]) in ast.dump(node)):
                line_number = node.lineno + self.offset()
                self.desugared_lines.insert(line_number,
                                            self.iter_start(node,
                                                            line,
                                                            line_num,
                                                            program_ast,
                                                            indentation))
                iterator_index = "".join(random.choice(string.ascii_uppercase) for _ in range(10))
                iterator_update = indentation + iterator_index + " += 1\n"
                self.desugared_lines.insert(line_number,
                                            indentation[:-4] + iterator_index + " = -1\n")
                self.desugared_lines.append(iterator_update)
                output = ("In iteration ' + str(" +
                          iterator_index +
                          ") + ', " +
                          variable_id +
                          " changed to ' + str(" +
                          variable_id +
                          ") ")
                return output
        raise KeyError("Could not find for loop")

    def scribe(self, line, program_ast):
        """The internal method called for basic printing of
        identifer, type, and value
        """
        variable_id, variable_type = utils.get_id_and_type(line, program_ast)
        label = utils.get_label(line, program_ast)
        output = (variable_id +
                  " is the ' + " +
                  variable_type +
                  " + ' ' + str(" +
                  variable_id +
                  ")")
        if len(self.filtered_labels) > 0:
            if not label or label not in self.filtered_labels:
                return ""
        if label:
            output += (" + ' (" + label + ")'")
        return output

    def variable_change(self, variable_id, line_num, indentation):
        """A helper method for watch that handles each line that watch
        identifies as a variable change"""
        desugared = variable_id + " changed to ' + str(" + variable_id + ")"
        action, ending = self.action_and_ending(line_num)
        if self.show_lines:
            output = indentation + action + self.from_line(line_num) + desugared + ending
        else:
            output = indentation + action + desugared + ending
        return output

    def watch(self, line, line_num, program_file, program_ast):
        variable_id, variable_type = utils.get_id_and_type(line, program_ast)
        self.watcher.watch_var(variable_id)
        lines = list(filter(lambda x: x > line_num,
                       utils.lines_variable_changed(variable_id, program_file)))
        self.watcher.set_lines(variable_id, lines)
        return ("Watching variable " +
                variable_id +
                ", currently ' + " +
                variable_type +
                " + ' ' + str(" +
                variable_id + ")")

def python_file_type(string):
    if not string.endswith(".py"):
        msg = "%r is not a Python file" % string
        raise argparse.ArgumentTypeError(msg)
    return string

def process_args():
    parser = argparse.ArgumentParser(description='Let PyScribe make print debugging easier and more efficient.')
    parser.add_argument('python_file', metavar='f', type=python_file_type, nargs='+',
                        help='The Python file with PyScribe API calls.')
    parser.add_argument('-d', '--desugared', action='store_true',
                        help='Produce a desugared version of the file with all API calls replaced with valid Python.')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Produce a clean version of the file with all references to PyScribe removed')
    parser.add_argument('-e', '--extraargs', nargs="+",
                        help='Arguments intended to be passed to Python file when run.')
    parser.add_argument('-l', '--log', action="store_true",
                        help='Log the files in a pyscribe_logs.txt file.')
    parser.add_argument('-n', '--nolines', action="store_true",
                        help='Don\'t show the line numbers from each call.')
    return parser.parse_args()

def main():
    args = process_args()
    scribe = Runner(args.log, args.nolines)
    program_file = args.python_file[0]
    line_mapping = scribe.gen_line_mapping(program_file)
    program_ast = scribe.gen_ast(program_file)
    desugared_copy = scribe.gen_desugared(line_mapping,
                                          program_file,
                                          program_ast)

    do_run = not args.clean and not args.desugared
    if args.clean:
        scribe.gen_clean_copy(program_file, line_mapping)
    if do_run:
        if args.extraargs:
            subprocess.call(['python', desugared_copy] + [arg for arg in args.extraargs])
        else:
            subprocess.call(['python', desugared_copy])
    if not args.desugared:
        os.remove(desugared_copy)

if __name__ == "__main__":
    main()
