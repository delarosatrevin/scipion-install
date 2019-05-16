#!/usr/bin/env python

import os
import sys


# ============ VARIABLES ======================================================

INSTALL_FOLDER = os.path.abspath('scipion')

SCIPION_GIT_REMOTE = 'https://github.com/delarosatrevin/scipion.git'
SCIPION_GIT_BRANCH = 'sdevel2'
J = 8

BUILD_OPENSSL = True
BUILD_OPENMPI = True
BUILD_FFTW = True
BUILD_JAVA = True

# =============================================================================

SCIPION_HOME = os.path.join(INSTALL_FOLDER, 'v2.0.0')
print("$SCIPION_HOME=%s" % SCIPION_HOME)

SCIPION_SW = os.path.join(INSTALL_FOLDER, 'SW')
SCIPION_SW = os.path.join(INSTALL_FOLDER, 'EM')
SCIPION = '%s/scipion --config %s/config/scipion.conf' % (SCIPION_HOME, SCIPION_HOME)


def createDir(d):
    if os.path.exists(d):
        print("ERROR: folder '%s' already exists. " % d)
        sys.exit(1)
    print("Creating folder '%s'..." % d)
    os.makedirs(d)


def system(cmd, printOnly=False):
    """ Print and execute a command. """
    print(">>> %s " % cmd.replace(SCIPION_HOME, '$SCIPION_HOME'))
    if not printOnly:
        os.system(cmd)


def updateConfig(inputConf, outputConf, replaceDict):
    """ Update the configuration file by replacing the
    entries in the 'replaceDict'.
    """
    def _updateLine(line):
        if line.strip():
            k = line.split()[0]
            if k in replaceDict:
                return '%s = %s\n' % (k, replaceDict[k])
        return line

    with open(inputConf) as f:
        fo = open(outputConf, 'w')
        for line in f:
            fo.write(_updateLine(line))
        fo.close()


def scipionInstall(args, j=J, printOnly=False):
    cmd = '%s install -j %d %s' % (SCIPION, j, args)
    system(cmd, printOnly=printOnly)


def scipionPython(args, printOnly=False):
    cmd = '%s python %s' % (SCIPION, args)
    system(cmd, printOnly=printOnly)


def scipionPipInstall(args, printOnly=False):
    newArgs = '-m pip install %s' % args
    scipionPython(newArgs, printOnly=printOnly)


def _initialSetup():
    system('rm -rf %s' % INSTALL_FOLDER)
    createDir(INSTALL_FOLDER)
    system('cp scipion.bashrc %s/' % INSTALL_FOLDER)

    os.chdir(INSTALL_FOLDER)

    for d in ['SW', 'EM', 'TESTDATA']:
        createDir(d)

    system('cd SW; ln -s ../EM em; mkdir tmp; mkdir log; cd ..;')

    system("git clone %s %s" % (SCIPION_GIT_REMOTE, SCIPION_HOME))
    os.chdir(SCIPION_HOME)
    system("git checkout %s" % SCIPION_GIT_BRANCH)

    system("echo 'This is a TEMPORARY COPY'")
    system(" cp ~/work/development/scipion-devel/pyworkflow/install/script.py "
           "%s/pyworkflow/install/script.py" % SCIPION_HOME)

    system("rm -rf software; ln -s ../SW software")
    system("mkdir data; cd data; ln -s ../../TESTDATA tests")

    system("mkdir config")
    for prefix in ['protocols', 'hosts']:
        system('cp pyworkflow/templates/%s.template config/%s.conf' % (prefix, prefix))

    scipionTemp = os.path.join(SCIPION_HOME, 'pyworkflow', 'templates', 'scipion.template')
    scipionConf = os.path.join(SCIPION_HOME, 'config', 'scipion.conf')

    print("Updating %s -> %s..." % (scipionTemp, scipionConf))
    replaceDict = {
        'OPENCV': 'False',
        'OPENCV_VER': '',
        'CUDA_LIB': '',
        'CUDA_BIN': '',
        'NVCC': '',
        'NVCC_INCLUDE': ''
    }

    # First create a basic config to build minimal requirements
    updateConfig(scipionTemp, scipionConf, replaceDict)


def _buildBasic():
    if BUILD_OPENSSL:
        scipionInstall('openssl')

    if BUILD_OPENMPI:
        scipionInstall('openmpi')
        replaceDict.update({'MPI_LIBDIR': 'software/lib',
                            'MPI_INCLUDE': 'software/include',
                            'MPI_BINDIR': 'software/bin'
                            })

    if BUILD_FFTW:
        scipionInstall('fftw3 fftw3f')

    if BUILD_JAVA:
        scipionInstall('java')
        replaceDict['JAVA_HOME'] = 'software/java8'

    # Update the config again with proper Java and OpenMPI
    updateConfig(scipionTemp, scipionConf, replaceDict)


def _buildScipion():
    scipionInstall('')  # install all Python and modules
    scipionPipInstall('scons mrcfile empiar_depositor pathlib2 poster jsonschema')

    os.chdir(INSTALL_FOLDER)
    system("git clone --recurse-submodules https://github.com/delarosatrevin/scipion-em-plugins.git plugins")


def _buildXmipp():
    os.chdir(os.path.join(SCIPION_SW, 'tmp'))
    system("git clone --recurse-submodules https://github.com/delarosatrevin/xmipp-bundle.git xmipp-bundle")
    os.chdir('xmipp-bundle')
    system('git submodule foreach "(git checkout master; git pull --prune)&"')
    # Build xmipp
    XMIPP = "%s python src/xmipp/xmipp" % SCIPION
    system('%s config' % XMIPP)
    system('%s compileAndInstall %d' % (XMIPP, J))
    system('mv build %s/xmipp' % SCIPION_EM)


if __name__ == '__main__':
    _initialSetup()
    _buildBasic()
    _buildScipion()
    _buildXmipp()
