import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    pyscribe_log.write('----------------------------------------\n' + 'x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x) + ' at beginning of for loop at line 4' + '\n')
    KPAPXCFLWN = -1
    for i in range(5):
        x += 1
        KPAPXCFLWN += 1
        pyscribe_log.write('From line 6: In iteration ' + str(KPAPXCFLWN) + ', x changed to ' + str(x) + '\n')

if __name__=="__main__":
    main()
