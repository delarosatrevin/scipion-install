#!/usr/bin/env python

import os

def system(cmd):
    print(cmd)   
    os.system(cmd)

for r in ['core', 'plugins']:
    rDir = os.path.join(os.environ['SCIPION_HOME'],  'source', r)
    dirs = os.listdir(rDir) 
    for d in dirs:
        dPath = os.path.join(rDir, d)
        system("cd %s && git pull --prune" % dPath)

