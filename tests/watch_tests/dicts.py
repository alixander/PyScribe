def main():
    ps = pyscriber.Scriber()
    x = {"a": 1}
    ps.watch(x)
    #x["a"] += 1
    #x["a"] = 3
    #x["b"] = 1

if __name__=="__main__":
    main()
