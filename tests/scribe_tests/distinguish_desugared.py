import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    pyscribe_log.write('From line 4: \n----------------------------------------\nx is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x) + '\n----------------------------------------\n'+ '\n')
    y = "hello"
    pyscribe_log.write('From line 6: \n****************************************\ny is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y) + '\n****************************************\n'+ '\n')
    pyscribe_log.close()

    pyscribe_log.close()
if __name__=="__main__":
    main()
