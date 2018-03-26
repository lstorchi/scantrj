import os
import os.path

###############################################################################

def if_exist_rm (fname):
    if os.path.exists(fname):
        os.remove(fname)

###############################################################################

def if_exist (fname):

    while (not os.path.exists(fname)):
        continue

    return True

###############################################################################

def centroid (fset):

    n = len(fset)
    c = []

    prev = len(fset[0])
    for i in range(prev):
        c.append(0.0)

    for i in range(1,n):
        if (len(fset[i]) != prev):
            return None

    for i in range(n):
        for j in range(prev):
            c[j] = c[j] + fset[i][j]

    for j in range(prev):
        c[j] = c[j] /float(n)

    return c
