import ast
import sys

def main():
    with open(sys.argv[1], 'r') as f:
        program = f.read()
    f.close()
    print(ast.dump(ast.parse(program)))

if __name__=="__main__":
    main()
