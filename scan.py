import argparse
import pybel
import sys
import os

import os.path

CONVERTER = "/opt/schrodinger/utilities/structconvert"
STMAP = "/opt/schrodinger/sitemap"

###############################################################################

def if_exist_rm (fname):
    if os.path.exists(fname):
        os.remove(fname)

###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="multipdb file", type=str)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

readlist = list(pybel.readfile("pdb", args.file))
basename = os.path.splitext(args.file)[0]

print len(readlist), " in use "

idx = 1
for mol in readlist:
    ifname = basename + "_" + str(idx) + ".pdb" 
    ofname = basename + "_" + str(idx) + ".mae"

    if_exist_rm (ifname)
    if_exist_rm (ofname)

    cmd = CONVERTER + " -ipdb " + ifname + " -omae " + ofname 
    mol.write("pdb", ifname)
    os.system (cmd)

    cmd = STMAP + " -j " + basename + ".jrun -prot " + ofname

    os.system (cmd)

    idx = idx + 1
 
    exit()
