def main():
    ps = pyscriber.Scriber()
    x = 5
    ps.d(x)
    y = "hello"
    ps.d(y, unit="*")

if __name__=="__main__":
    main()
