import re
import pprint
import pyscribe

def main():
    pyscribe_log = open('pyscribe_logs.txt', 'w')
    ps = pyscribe.Scriber()

    ps.save_logs(True)

    x = 5
    pyscribe_log.write('From line 9: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x)+ '\n')

    BSGPBKPBDB = -1
    pyscribe_log.write('----------------------------------------\n' + 'i is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(i))).group()[1:-1] + ' ' + str(i) + ' at beginning of for loop at line 11' + '\n')
    for i in xrange(5):
        BSGPBKPBDB += 1
        pyscribe_log.write('From line 12: In iteration ' + str(BSGPBKPBDB) + ', i changed to ' + str(i) + '\n')

    y = "hello"
    pyscribe_log.write('From line 15: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')
    pyscribe_log.write('From line 16: Watching variable y, currently ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y)+ '\n')

    y = "world"

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    pyscribe_log.write('From line 21: synonyms is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(synonyms))).group()[1:-1] + ' ' + str(synonyms)+ '\n')

    pyscribe_log.close()
if __name__ == "__main__":
    main()
