import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    for i in range(5):
        x += i
        pyscribe_log.write('From line 6: '+ '\n')

if __name__=="__main__":
    main()
