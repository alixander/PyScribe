import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    pyscribe_log.write('----------------------------------------\n' + 'x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x) + ' at beginning of for loop at line 4' + '\n')
    QFWEABMSUZ = -1
    for i in range(5):
        x += 1
        QFWEABMSUZ += 1
        pyscribe_log.write('From line 6: In iteration ' + str(QFWEABMSUZ) + ', x changed to ' + str(x) + '\n')
    pyscribe_log.close()

if __name__=="__main__":
    main()
