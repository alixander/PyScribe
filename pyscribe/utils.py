import ast
import re

def draw_line(unit="-"):
    output = ""
    for _ in range(40):
        output += unit
    return output + "\\n"

def get_indentation(line):
    return line[:len(line)-len(line.lstrip())]

def get_node(match, program_ast):
    for node in ast.walk(program_ast):
        if match == ast.dump(node):
            return node
    raise KeyError("Could not find node")

def get_variable_id(line, program_ast):
    """Return the variable id by finding the line in the program AST
    and gettings its argument
    """
    parsed_line = ast.dump(ast.parse(line).body[0])
    node = get_node(parsed_line, program_ast)
    return node.value.args[0].id

def get_label(line, program_ast):
    parsed_line = ast.dump(ast.parse(line).body[0])
    node = get_node(parsed_line, program_ast)
    if len(node.value.keywords) > 0 and node.value.keywords[0].arg == 'label':
        return node.value.keywords[0].value.s
    return None

def get_filtered_labels(line, program_ast):
    indentation = get_indentation(line)
    line = line[len(indentation):]
    parsed_line = ast.dump(ast.parse(line).body[0])
    node = get_node(parsed_line, program_ast)
    filtered_labels = []
    if len(node.value.keywords) > 0 and node.value.keywords[0].arg == 'filtered':
        for label in node.value.keywords[0].value.elts:
            filtered_labels.append(label.s)
    return filtered_labels

def is_shebang(line):
    return True if "#!/usr/bin" in line else False

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
    assign_pat = variable_id + r'[\s]*(\+|\-|\*|\/)?=.*\n'
    list_mutation_pat = variable_id + r'\.(append|extend|insert|remove|pop|reverse)(.)*\n'
    dict_mutation_pat = variable_id + r'\[[\"a-zA-Z0-9]+\](\s)?(\+|\-|\*|\/)?='
    key_del_pat = r'del[\s]?' + variable_id
    for line_num, line_content in enumerate(program.readlines()):
        assign = re.search(assign_pat, line_content)
        list_mutation = re.search(list_mutation_pat, line_content)
        dict_mutation = re.search(dict_mutation_pat, line_content)
        dict_key_deleted = re.search(key_del_pat, line_content)
        changed = assign or list_mutation or dict_mutation or dict_key_deleted
        if changed:
            lines.append(line_num)
    program.close()
    return lines

def get_timestamp(indentation):
    timestamp = (indentation +
                 "pyscribe_log.write('" +
                 draw_line(unit="%") +
                 "Log saved at ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\\n" +
                 draw_line(unit="%") +
                 "\\n')\n")
    return timestamp

def get_end(indentation):
    end = (indentation +
           "pyscribe_log.write('\\n" +
           draw_line(unit="%") +
           "End of log\\n" +
           draw_line(unit="%") +
           "')\n")
    return end
