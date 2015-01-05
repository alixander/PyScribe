def main():
    ps = pyscriber.Scriber()
    x = set([1, 2])
    ps.watch(x)
    x.add(3)
    x.discard(1)
    x.clear()

if __name__=="__main__":
    main()
