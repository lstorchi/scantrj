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
