import argparse
from pysat.solvers import Glucose4

def get_f(n, k):
    f = []
    vars = {}
    n += 1
    k += 1

    # Set all vars
    # and rule that each edge at least is painted
    t = 1
    S1 = []
    for i in range(1, n-1):
        for j in range(i+1, n):
            dis = []
            for c in range(1, k):
                vars[(i,j,c)] = t
                dis.append(t)
                t += 1

            S1.append(dis)

    f.extend(S1)

    # Each edge is painted in only one color
    S2 = []
    for i in range(1, n-1):
        for j in range(i+1, n):
            for c1 in range(1, k-1):
                dis = []
                for c2 in range(c1+1, k):
                    dis.append(-vars[(i,j,c1)])
                    dis.append(-vars[(i,j,c2)])

                S2.append(dis)

    f.extend(S2)

    # Each triangle is not painted in one color
    S3 = []
    for i in range(1, n-2):
        for j in range(i+1, n-1):
            for l in range(j+1, n):
                for c in range(1, k):
                    dis = []
                    dis.append(-vars[(i,j,c)])
                    dis.append(-vars[(j,l,c)])
                    dis.append(-vars[(i,l,c)])
                    S3.append(dis)

    f.extend(S3)

    return f

def find_max_clique(k):
    clique = 2
    n = 2

    while True:
        f = get_f(n, k)

        with Glucose4(bootstrap_with=f) as sat:
            if sat.solve():
                clique = n
            else:
                break

        print("Clique {} for k={} exists".format(n, k))
        n += 1

    print("Max clique for k={} is {}".format(k, clique))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find max clique painted in k colors such that each triangle is not painted in one color")
    parser.add_argument('k', type=int, help="Number of colors")

    args = parser.parse_args()

    if args.k <= 0:
        raise Exception("k should be > 0")

    find_max_clique(args.k)

