#!/usr/bin/env python

import os
import sys


here = os.path.dirname(os.path.realpath(__file__))
levelUp = os.path.dirname(here)
sys.path.append(levelUp)

import build_scipion as bs

n = len(sys.argv)
installFolder = os.path.abspath(sys.argv[1] if n > 1 else '/usr/local/scipion')

print("Installing in: %s" % installFolder)


class MyBuild(bs.Build):
    @classmethod
    def deps(cls):
        cls.system("sudo apt-get install gcc-5 g++-5 cmake openjdk-8-jdk "
                   "libxft-dev libssl-dev libxext-dev libxml2-dev libreadline6 "
                   "libquadmath0 libxslt1-dev libopenmpi-dev openmpi-bin  "
                   "libxss-dev libgsl0-dev libx11-dev gfortran libfreetype6-dev "
                   "libopencv-dev curl git")

    @classmethod
    def copyConfig(cls, *names):
        for confName in names:
            cls.system("cp %s/%s.conf %s"
                       % (here, confName, cls.SCIPION_CONF % confName))


# Initialize folder structure
MyBuild.init(installFolder, clean=True)

# Install dependencies
MyBuild.deps()

# Overwrite some configuration files
MyBuild.copyConfig('scipion', 'hosts')

# Copy update script
MyBuild.system('cp %s/update_scipion2.x %s/' % (here, installFolder))

# Add alias to /etc/bashrc
MyBuild.system('printf "\n# Alias to load Scipion2\n'
               'alias load_scipion2=\'. %s/scipion.bashrc\'\n\n" '
               '>> /etc/bashrc' % installFolder)

# Build Scipion
MyBuild.scipion()

# Build Xmipp
MyBuild.xmipp()



