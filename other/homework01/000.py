x = y = 1
while x <= 9:
    while y <= x:
        print("%d*%d=%-2d" % (y, x, x*y), end="  ")
        y += 1
    print()
    x += 1
    y = 1
