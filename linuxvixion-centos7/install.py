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
        cls.system("yum -y install wget gcc-c++ glibc-headers gcc gcc-g++ cmake "
                   "java-1.8.0-openjdk-devel.x86_64 libXft-devel.x86_64  "
                   "openssl-devel.x86_64 libXext-devel.x86_64  libxml++.x86_64 "
                   "libquadmath-devel.x86_64 libxslt.x86_64 openmpi-devel.x86_64  "
                   "gsl-devel.x86_64  libX11.x86_64  gcc-gfortran.x86_64")

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



