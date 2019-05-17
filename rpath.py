#!/usr/bin/env python

import os
import sys
import subprocess


inputFolder = sys.argv[1]

files = os.listdir(inputFolder)

RPATH_ROOT = '/home/josem/work/development/scipion-binary/scipion/v2.0.0/software/lib'

def isElf(f):
    return (os.path.isfile(f) and not os.path.islink(f) and open(f).read(4) == '\x7fELF')


def getElfRpath(f):
    rpath = ''
    try:
        output = subprocess.check_output("chrpath %s" % f, shell=True)
        if 'RPATH=' in output:
            rpath = output.split('RPATH=')[1].strip()
    except:
        pass

    return rpath


for root, dirnames, filenames in os.walk(inputFolder, topdown=True):
    if 'tmp' in dirnames:
        dirnames.remove('tmp')

    if 'xmipp' in dirnames:
        dirnames.remove('xmipp')

    if 'java8' in dirnames:
        dirnames.remove('java8')

    for fname in filenames:
        fpath = os.path.join(root, fname)
        if isElf(fpath):
            rpath = getElfRpath(fpath)
            if rpath:
                print("\n%s" % fpath)
                print("   RPATH: %s" % getElfRpath(fpath))
                #os.system('chrpath %s' % fpath)
                if rpath == RPATH_ROOT:
                    os.system("chrpath %s -r '$ORIGIN:$ORIGIN/../lib'" % fpath)
                    #print("chrpath %s -r '$ORIGIN:$ORIGIN/../lib'" % fpath)
		
