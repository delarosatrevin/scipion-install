#!/usr/bin/env python

import os
import sys


here = os.path.dirname(os.path.realpath(__file__))
levelUp = os.path.dirname(here)
sys.path.append(levelUp)

import build_scipion as bs

n = len(sys.argv)
bs.INSTALL_FOLDER = os.path.abspath(sys.argv[1] if n > 1 else '/usr/local/scipion')

print(bs.INSTALL_FOLDER)


class MyBuild(bs.Build):
    @classmethod
    def deps(cls):
        bs.system("yum -y install wget gcc-c++ glibc-headers gcc gcc-g++ cmake "
                  "java-1.8.0-openjdk-devel.x86_64 libXft-devel.x86_64  "
                  "openssl-devel.x86_64 libXext-devel.x86_64  libxml++.x86_64 "
                  "libquadmath-devel.x86_64 libxslt.x86_64 openmpi-devel.x86_64  "
                  "gsl-devel.x86_64  libX11.x86_64  gcc-gfortran.x86_64")

    @classmethod
    def copyConfig(cls, *names):
        for confName in names:
            bs.system("cp %s/%s.conf %s"
                      % (here, confName, bs.scipionConf % confName))


# Initialize folder structure
MyBuild.init()

# Install dependencies
MyBuild.deps()

# Overwrite some configuration files
MyBuild.copyConfig('scipion', 'hosts')

# Build Scipion
MyBuild.scipion()

# Build Xmipp
MyBuild.xmipp()



