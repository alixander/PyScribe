import re
def main():
    x = 5
    print('From line 3: x is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(x))).group()[1:-1] + ' ' + str(x))
    y = "hello"
    print('From line 5: y is the ' + re.search(r'\'[a-zA-Z]*\'', str(type(y))).group()[1:-1] + ' ' + str(y))
    y = "world"

if __name__=="__main__":
    main()
