#!/usr/bin/env python

import os
import sys

if not os.geteuid()==0:
    print("Scipion update command should be run as root")
    sys.exit(1)

print("Updating your LinuxVixion, S.L. Certified Scipion2 installation.")
print("It will take approximately 5 minutes to complete.")

def system(cmd):
    print(cmd)   
    os.system(cmd)

for r in ['core', 'plugins']:
    rDir = os.path.join(os.environ['SCIPION_HOME'],  'source', r)
    dirs = os.listdir(rDir) 
    for d in dirs:
        dPath = os.path.join(rDir, d)
        system("cd %s && git pull --prune" % dPath)

