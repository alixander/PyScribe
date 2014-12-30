import pyscribe

def main():
    ps = pyscribe.Scriber()

    ps.save_logs(True)

    x = 5
    ps.p(x)

    for i in xrange(5):
        ps.iterscribe(i)

    y = "hello"
    ps.p(y)
    ps.watch(y)

    y = "world"

    synonyms = {"clerk": "secretary", "student": "apprentice", "ground": "floor"}
    ps.p(synonyms)

if __name__ == "__main__":
    main()
