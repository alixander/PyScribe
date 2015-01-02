def main():
    ps = pyscribe.Scriber(filtered=["word"])
    x = 5
    ps.p(x, label="number")
    y = "hello"
    ps.p(y, label="word")
    ps.p(y)

if __name__=="__main__":
    main()
