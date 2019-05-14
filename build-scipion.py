#!/usr/bin/env python

import os
import sys


# ============ VARIABLES ======================================================

INSTALL_FOLDER = 'scipion'

SCIPION_GIT_REMOTE = 'https://github.com/delarosatrevin/scipion.git'
SCIPION_GIT_BRANCH = 'sdevel2'
J = 8

# =============================================================================


def createDir(d):
    if os.path.exists(d):
        print("ERROR: folder '%s' already exists. " % d)
        sys.exit(1)
    print("Creating folder '%s'..." % d)
    os.makedirs(d)


def system(cmd):
    """ Print and execute a command. """
    print(">>> %s " % cmd)
    os.system(cmd)

system('rm -rf %s' % INSTALL_FOLDER)

createDir(INSTALL_FOLDER)
os.chdir(INSTALL_FOLDER)

for d in ['SW', 'EM', 'TESTDATA']:
    createDir(d)

system('cd SW; ln -s ../EM em; mkdir tmp; mkdir log; cd ..;')

SCIPION_HOME = 'v2.0.0'

system("git clone %s %s" % (SCIPION_GIT_REMOTE, SCIPION_HOME))
os.chdir(SCIPION_HOME)
system("echo 'This is a TEMPORARY COPY'")
system("echo PWD: $PWD")
system(" cp ~/work/development/scipion-devel/pyworkflow/install/script.py "
       "pyworkflow/install/script.py")
system("git checkout %s" % SCIPION_GIT_BRANCH)
system("rm -rf software; ln -s ../SW software")
system("mkdir data; cd data; ln -s ../../TESTDATA tests")


system("mkdir config")
for prefix in ['scipion', 'protocols', 'hosts']:
    system('cp pyworkflow/templates/%s.template config/%s.conf' % (prefix, prefix))

system("./scipion --config config/scipion.conf install openmpi openssl fftw3 fftw3f -j %d" % J)

#system("git clone %s %s" % (SCIPION_GIT_REMOTE, 'V2.0.0'))
#system("git clone %s %s" % (SCIPION_GIT_REMOTE, 'V2.0.0'))


