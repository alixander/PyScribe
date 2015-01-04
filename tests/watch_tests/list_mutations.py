def main():
    ps = pyscriber.Scriber()
    x = [1, 2]
    ps.watch(x)
    x.append(3)
    x.reverse()
    y = ["hi"]
    y.extend(x)  # Not watching y so this should do nothing

if __name__=="__main__":
    main()
