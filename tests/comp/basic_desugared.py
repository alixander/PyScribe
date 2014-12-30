import re
import pprint
from pyscribe import pyscribe

def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    ps = pyscribe.Scriber()

    ps.save_logs(True)

    x = 5
    pyscribe_log.write('From line 9: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x)+ '\n')

    bar = "foo"
    TLJVHZKTOY = -1
    pyscribe_log.write('----------------------------------------\n' + 'bar is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(bar))).group()[1:-1] + ' ' + str(bar) + ' at beginning of for loop at line 12' + '\n')
    for i in xrange(5):
        bar += str(i)
        TLJVHZKTOY += 1
        pyscribe_log.write('From line 14: In iteration ' + str(TLJVHZKTOY) + ', bar changed to ' + str(bar) + '\n')

    y = "hello"
    pyscribe_log.write('From line 17: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')
    pyscribe_log.write('From line 18: Watching variable y, currently ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')

    y = "world"

    foo = 1234
    pyscribe_log.write('From line 23: \n----------------------------------------\nfoo is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(foo))).group()[1:-1] + ' ' + str(foo) + '\n----------------------------------------\n'+ '\n')
    pyscribe_log.write('From line 24: \n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nfoo is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(foo))).group()[1:-1] + ' ' + str(foo) + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'+ '\n')

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    pyscribe_log.write('From line 27: synonyms is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(synonyms))).group()[1:-1] + ' ' + str(synonyms)+ '\n')

    pyscribe_log.close()
if __name__ == "__main__":
    main()
