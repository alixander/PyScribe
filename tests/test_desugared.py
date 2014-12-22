def main():
    ps = pyscriber.Scriber()
    x = 5
    print('From line 3: x is the ' + type(x) + ' ' + str(x))
    y = "hello"
    print('From line 5: y is the ' + type(y) + ' ' + str(y))
    y = "world"

if __name__=="__main__":
    main()
