#!/usr/bin/env python

import os
import sys


# ============ VARIABLES ======================================================

SCIPION_GIT_REMOTE = 'https://github.com/delarosatrevin/scipion.git'
SCIPION_GIT_BRANCH = 'sdevel2'

SCIPION_GIT_REMOTE = 'https://github.com/I2PC/scipion.git'
SCIPION_GIT_BRANCH = 'master'

PLUGINS_GIT_REMOTE = 'https://github.com/delarosatrevin/scipion-em-plugins.git'
XMIPP_GIT_REMOTE = 'https://github.com/delarosatrevin/xmipp-bundle.git'


J = 8

BUILD_OPENSSL = True
BUILD_OPENMPI = True
BUILD_FFTW = True
BUILD_JAVA = True

# =============================================================================


class Build:
    @classmethod
    def initVars(cls, installFolder):
        cls.INSTALL_FOLDER = installFolder
        cls.SCIPION_HOME = os.path.join(installFolder, 'v2.0.0')
        print("$SCIPION_HOME=%s" % cls.SCIPION_HOME)

        cls.SCIPION_SW = os.path.join(cls.INSTALL_FOLDER, 'SW')
        cls.SCIPION_EM = os.path.join(cls.INSTALL_FOLDER, 'EM')
        cls.SCIPION = ('%s/scipion --config %s/config/scipion.conf'
                       % (cls.SCIPION_HOME, cls.SCIPION_HOME))

        cls.SCIPION_TEMP = os.path.join(cls.SCIPION_HOME,
                                        'pyworkflow', 'templates', '%s.template')
        cls.SCIPION_CONF = os.path.join(cls.SCIPION_HOME,
                                        'config', '%s.conf')

    replaceDict = {
        'OPENCV': 'False',
        'OPENCV_VER': '',
        'CUDA_LIB': '',
        'CUDA_BIN': '',
        'NVCC': '',
        'NVCC_INCLUDE': ''
    }

    @classmethod
    def system(cls, cmd, printOnly=False):
        """ Print and execute a command. """
        print(">>> %s " % cmd.replace(cls.SCIPION_HOME, '$SCIPION_HOME'))
        if not printOnly:
            os.system(cmd)

    @classmethod
    def createDir(cls, d, clean=False):
        if os.path.exists(d):
            if clean:
                cls.system("rm -rf %s" % d)
            else:
                print("ERROR: folder '%s' already exists. " % d)
            sys.exit(1)
        print("Creating folder '%s'..." % d)
        os.makedirs(d)

    @classmethod
    def updateConfig(cls, confName, replaceDict):
        """ Update the configuration file by replacing the
        entries in the 'replaceDict'.
        """
        inputConf = cls.SCIPION_TEMP % confName
        outputConf = cls.SCIPION_CONF % confName

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

    @classmethod
    def scipionInstall(cls, args, j=J, printOnly=False):
        cmd = '%s install -j %d %s' % (cls.SCIPION, j, args)
        cls.system(cmd, printOnly=printOnly)

    @classmethod
    def scipionPython(cls, args, printOnly=False):
        cmd = '%s python %s' % (cls.SCIPION, args)
        cls.system(cmd, printOnly=printOnly)

    @classmethod
    def scipionPipInstall(cls, args, printOnly=False):
        newArgs = '-m pip install %s' % args
        cls.scipionPython(newArgs, printOnly=printOnly)

    @classmethod
    def init(cls, installFolder, clean=False):
        cls.initVars(installFolder=installFolder)

        cls.system('rm -rf %s' % cls.INSTALL_FOLDER)
        cls.createDir(cls.INSTALL_FOLDER, clean=clean)
        cls.system('cp scipion.bashrc %s/' % cls.INSTALL_FOLDER)

        os.chdir(cls.INSTALL_FOLDER)

        for d in ['SW', 'EM', 'TESTDATA']:
            cls.createDir(d)

        cls.system('cd SW; ln -s ../EM em; mkdir tmp; mkdir log; cd ..;')

        cls.system("git clone %s %s" % (SCIPION_GIT_REMOTE, cls.SCIPION_HOME))
        os.chdir(cls.SCIPION_HOME)
        cls.system("git checkout %s" % SCIPION_GIT_BRANCH)

        # cls.system("echo 'This is a TEMPORARY COPY'")
        # cls.system(" cp ~/work/development/scipion-devel/pyworkflow/install/script.py "
        #        "%s/pyworkflow/install/script.py" % cls.SCIPION_HOME)

        cls.system("rm -rf software; ln -s ../SW software")
        cls.system("mkdir data; cd data; ln -s ../../TESTDATA tests")

        cls.system("mkdir config")
        for prefix in ['protocols', 'hosts']:
            cls.system('cp pyworkflow/templates/%s.template config/%s.conf' % (prefix, prefix))

        # First create a basic config to build minimal requirements
        cls.updateConfig('scipion', cls.replaceDict)

    @classmethod
    def deps(cls):
        if BUILD_OPENSSL:
            cls.scipionInstall('openssl')

        if BUILD_OPENMPI:
            cls.scipionInstall('openmpi')
            cls.replaceDict.update({'MPI_LIBDIR': 'software/lib',
                                'MPI_INCLUDE': 'software/include',
                                'MPI_BINDIR': 'software/bin'
                                })

        if BUILD_FFTW:
            cls.scipionInstall('fftw3 fftw3f')

        if BUILD_JAVA:
            cls.scipionInstall('java')
            cls.replaceDict['JAVA_HOME'] = 'software/java8'

            # Update the config again with proper Java and OpenMPI
            cls.updateConfig('scipion', cls.replaceDict)

    @classmethod
    def scipion(cls):
        cls.scipionInstall('')  # install all Python and modules
        cls.scipionPipInstall('scons mrcfile empiar_depositor pathlib2 poster jsonschema')

        os.chdir(cls.INSTALL_FOLDER)
        cls.system("git clone --recurse-submodules %s plugins" % PLUGINS_GIT_REMOTE)

    @classmethod
    def xmipp(cls):
        os.chdir(os.path.join(cls.SCIPION_SW, 'tmp'))
        cls.system("git clone --recurse-submodules %s xmipp-bundle" % XMIPP_GIT_REMOTE)
        os.chdir('xmipp-bundle')
        cls.system('git submodule foreach "(git checkout master; git pull --prune)&"')
        # Build xmipp
        XMIPP = "%s python src/xmipp/xmipp" % cls.SCIPION
        cls.system('%s config' % XMIPP)
        cls.system('%s compileAndInstall %d' % (XMIPP, J))
        cls.system('mv build %s/xmipp' % cls.SCIPION_EM)


if __name__ == '__main__':
    pass
    # _initialSetup()
    # _buildBasic()
    # _buildScipion()
    # _buildXmipp()
