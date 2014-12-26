def main():
    ps = pyscriber.Scriber()
    x = 5
    for i in range(5):
        x += 1
        ps.iterscribe(x)

if __name__=="__main__":
    main()
