import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    pyscribe_log.write('From line 4: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x)+ '\n')
    y = "hello"
    pyscribe_log.write('From line 6: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')
    a = [1, 2, 3]
    pyscribe_log.write('From line 8: a is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(a))).group()[1:-1] + ' ' + str(a)+ '\n')
    b = {1: "a", 2: "b"}
    pyscribe_log.write('From line 10: b is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(b))).group()[1:-1] + ' ' + str(b)+ '\n')

    pyscribe_log.close()
if __name__=="__main__":
    main()
