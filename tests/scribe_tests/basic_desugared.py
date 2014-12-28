import re
import pprint
def main():
    x = 5
    print('From line 4: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x))
    y = "hello"
    print('From line 6: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y))

if __name__=="__main__":
    main()
