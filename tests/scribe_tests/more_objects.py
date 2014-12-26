def main():
    ps = pyscriber.Scriber()
    x = 5
    ps.p(x)
    y = "hello"
    ps.p(y)
    a = [1, 2, 3]
    ps.p(a)
    b = {1: "a", 2: "b"}
    ps.p(b)

if __name__=="__main__":
    main()
