from pyscribe import pyscribe

def main():
    ps = pyscribe.Scriber()

    x = 5
    ps.p(x)

    bar = "foo"
    for i in xrange(5):
        bar += str(i)
        ps.iterscribe(bar)

    y = "hello"
    ps.p(y)
    ps.watch(y)

    y = "world"

    foo = 1234
    ps.d(foo)
    ps.d(foo, unit="^")

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    ps.p(synonyms)

if __name__ == "__main__":
    main()
