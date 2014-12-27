import re
import pprint
def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    x = 5
    pyscribe_log.write('From line 4: Watching variable x, currently ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x)+ '\n')
    x = 3
    pyscribe_log.write('From line 5: x changed to ' + str(x)+ '\n')
    y = "world"
    x = 7
    pyscribe_log.write('From line 7: x changed to ' + str(x)+ '\n')
    pyscribe_log.close()

    pyscribe_log.close()
if __name__=="__main__":
    main()
