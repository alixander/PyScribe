import ast
import re

def draw_line(unit="-"):
    output = ""
    for _ in xrange(40):
        output += unit
    return output + "\\n"

def get_indentation(line):
    return line[:len(line)-len(line.lstrip())]

def get_variable_id(line, program_ast):
    """Return the variable id by finding the line in the program AST
    and gettings its argument
    """
    parsed_line = ast.dump(ast.parse(line).body[0])
    for node in ast.walk(program_ast):
        if parsed_line == ast.dump(node):
            return node.value.args[0].id
    raise KeyError("Was not able to find variable ID")

def get_id_and_type(line, program_ast):
    variable_id = get_variable_id(line, program_ast)
    variable_type = ("re.search(r\'\\\'[a-zA-Z]*\\\'\', str(type(" +
                     variable_id +
                     "))).group()[1:-1]")
    return (variable_id, variable_type)

def get_distinguish_unit(line, program_ast):
    parsed_line = ast.dump(ast.parse(line).body[0])
    for node in ast.walk(program_ast):
        if parsed_line == ast.dump(node) and node.value.keywords:
            return node.value.keywords[0].value.s
    return "-"

def lines_variable_changed(variable_id, program_file):
    lines = []
    program = open(program_file, 'r')
    change_pattern = variable_id + r'[\s]*=[\sa-zA-Z0-9]*\n'
    for line_num, line_content in enumerate(program.readlines()):
        match = re.search(change_pattern, line_content)
        if match:
            lines.append(line_num)
    program.close()
    return lines

