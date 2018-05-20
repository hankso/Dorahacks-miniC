def tmp(b, c):
    print("%d" % (b))
    return c

def main():
    b = 2.0
    a = 1 + b
    print("hello world");
    a = tmp(b, a)
    print("%d" % (a))
    p_e = 99
    p_f = p_e * p_e
    aaaaa = \
    {
        "tt": None,
        "rr": None,
    }
    aa = [aaaaa.copy() for i in range(5)]
    c = 0
    while c<10:
        print("-+%d+-" % (c))
        c++
    if (a == 3.0):
        print("a equals to 3.0")
    while (a > 0):
        a -= 1
        print("current a: %d" % (a))
    return 0
if __name__ == "__main__":
    main()
