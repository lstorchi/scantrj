import numpy
import sys
import os
import re

import numpy.linalg

sys.path.append("./common")
import util

fname = ""

if len(sys.argv) != 2:
    print("usage: " + sys.argv[0] + " litofpdbs.txt")
    exit(1)
else:
    fname = sys.argv[1]

with open(fname) as file:
    for fname in file:
        name = fname.replace('\n', '')
        fp = open(name, "r")
        points = []
        for line in fp:
            if (line.startswith("HETATM")):
                sline = line.split()
                if len(sline) != 11:
                    print("Error in ", name, " at ", line )
                    exit(1)
                points.append((float(sline[5]), \
                    float(sline[6]), \
                    float(sline[7])))

        c = util.centroid(points)

        covm = numpy.cov (points, rowvar=False)

        ueigs, eigvls =  numpy.linalg.eig(covm)
        eigs =  numpy.sort(ueigs)

        linearity = 0.0
        planarity = 0.0
        sphericity = 0.0
        anisotropy = 0.0

        if  eigs.size == 3:
            sum = numpy.sum(eigs)
            l1 = eigs[2]/sum
            l2 = eigs[1]/sum
            l3 = eigs[0]/sum
            linearity = (l1 - l2)/l1
            planarity = (l2 - l3) / l1
            sphericity = l3 / l1
            anisotropy = (l1 - l3)/l1
        else:
            print("Error in eigenvalues dimension")

        print("%s, %12.5f, %12.5f, %12.5f, %12.5f"%( \
            name, linearity, planarity, sphericity, anisotropy))
        fp.close() 