import argparse
import pybel
import sys
import os

import os.path

import gzip
import shutil

sys.path.append("./common")
import util

CONVERTER = "/usr/local/schrodinger/utilities/structconvert"
STMAP = "/usr/local/schrodinger/sitemap"

###############################################################################

def wait_for_list_of_files (listoffiles):

    for fname in listoffiles:
        if_exist (fname)

###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="multipdb file", type=str)
parser.add_argument("-n","--numofrun", help="num of parallel run", type=int,\
        default=0)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

readlist = list(pybel.readfile("pdb", args.file))
basename = os.path.splitext(args.file)[0]

numofrun = args.numofrun
if numofrun == 0:
    numofrun = len(readlist)

print len(readlist), " in use "

idx = 1
localidx = 1
files_to_wait_for = []
for mol in readlist:
    noewbasename = basename + "_" + str(idx)
    ifname = noewbasename + ".pdb" 
    ofname = noewbasename + ".mae"

    util.f_exist_rm (ifname)
    util.if_exist_rm (ofname)

    cmd = CONVERTER + "-sitebox 6 -reportsize 10 -resolution fine -ipdb " \
            + ifname + " -omae " + ofname 
    mol.write("pdb", ifname)
    os.system (cmd)

    
    cmd = STMAP + " -j " + noewbasename + ".jrun -prot " + ofname

    os.system (cmd)

    files_to_wait_for.append(noewbasename + ".jrun_out.maegz")
    
    idx = idx + 1

    if (localidx > numofrun):
        wait_for_list_of_files (files_to_wait_for)
        localidx = 0
        files_to_wait_for.clear()
