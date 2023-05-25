#!/usr/bin/env python

import os
import sys
import argparse
import subprocess


here = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


# ============ VARIABLES ======================================================
GITHUB_USER = 'scipion-em'
DEFAULT_BRANCH = 'master'

XMIPP_BRANCH = 'master'
XMIPP_USER = 'I2PC'

J = 8

BUILD_OPENSSL = True
BUILD_OPENMPI = True
BUILD_FFTW = True
BUILD_JAVA = True

# =============================================================================s

class ScipionInstaller:
    def __init__(self, installFolder=None, onlyPrint=False, useHttps=False, buildXmipp=False):
        self.INSTALL_FOLDER = os.path.abspath(installFolder or os.getcwd())
        self.onlyPrint = onlyPrint
        self.useHttps = useHttps
        self.buildXmipp = buildXmipp
        self.commands = []

        self.SCIPION_HOME = self.INSTALL_FOLDER
        self.commands = [
            "export SCIPION_HOME=%s" % self.SCIPION_HOME,
            'export PATH=$SCIPION_HOME/conda/bin:$PATH',
            'export LD_LIBRARY_PATH=$SCIPION_HOME/conda/lib:$LD_LIBRARY_PATH'
            ]

        self.ENV_ACTIVATE = ('export PATH=%s/conda/bin:$PATH; '
                             'export LD_LIBRARY_PATH=%s/conda/lib:$LD_LIBRARY_PATH'
                             % (self.SCIPION_HOME, self.SCIPION_HOME))

        self.SCIPION_EM = os.path.join(self.INSTALL_FOLDER, 'EM')
        self.SCIPION_SRC = os.path.join(self.INSTALL_FOLDER, 'source')
        self.SCIPION_TMP = os.path.join(self.INSTALL_FOLDER, 'tmp')
        self.SCIPION = ('%s/scipion --config %s/config/scipion.conf'
                       % (self.SCIPION_HOME, self.SCIPION_HOME))

        self.SCIPION_CONF = os.path.join(self.SCIPION_HOME, 'config')

        self.XMIPP_BUNDLE = os.path.join(self.SCIPION_SRC, 'xmipp-bundle')

    replaceDict = {
        'OPENCV': 'False',
        'OPENCV_VER': '',
        'CUDA_LIB': '',
        'CUDA_BIN': '',
        'NVCC': '',
        'NVCC_INCLUDE': ''
    }
    PLUGINS_LIST = [
        "scipion-em-appion",
        "scipion-em-atsas",
        "scipion-em-bamfordlab",
        "scipion-em-bsoft",
        "scipion-em-cistem",
        "scipion-em-cryoef",
        "scipion-em-eman2",
        "scipion-em-empiar",
        "scipion-em-emxlib",
        #"scipion-em-facilities",
        "scipion-em-gautomatch",
        "scipion-em-gctf",
        "scipion-em-imagic",
        "scipion-em-imod",
        #"scipion-em-ispyb",
        "scipion-em-localrec",
        "scipion-em-locscale",
        "scipion-em-motioncorr",
        "scipion-em-nysbc",

        "scipion-em-relion",
        "scipion-em-resmap",
        #"scipion-em-simple",
        #"scipion-em-sll",
        "scipion-em-sphire",
        "scipion-em-spider",
        "scipion-em-tomo",
        "scipion-em-topaz",
        #"scipion-em-xmipp",

        # modelling plugins
        "scipion-em-chimera",
        "scipion-em-ccp4",
        "scipion-em-phenix",
        "scipion-em-powerfit",
    ]

    def system(self, cmd):
        """ Print and execute a command. """
        cmdR = cmd.replace(self.SCIPION_HOME, '$SCIPION_HOME')
        self.commands.append(cmdR)

    def conda(self, args):
        """ Execute a conda command. Load the environment if needed. """
        self.system('conda %s' % args)

    def removeDir(self, d):
        self.system("rm -rf %s" % d)

    def createDir(self, d, clean=False):
        if os.path.exists(d):
            if clean:
                self.removeDir(d)
            else:
                print("ERROR: folder '%s' already exists. " % d)
                sys.exit(1)

        self.system("mkdir -p %s" % d)

    def updateConfig(self, confName, replaceDict):
        """ Update the configuration file by replacing the
        entries in the 'replaceDict'.
        """
        inputConf = self.SCIPION_TEMP % confName
        outputConf = self.SCIPION_CONF % confName

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

    def pipInstall(self, args):
        newArgs = 'python -m pip install %s' % args
        self.system(newArgs)

    def condaInstall(self, args, channel=''):
        newArgs = 'install -y %s ' % args
        if channel:
            newArgs += '-c %s' % channel
        self.conda(newArgs)

    def clone(self, name, user=None, devel=True, outputDir='', branch='master',
              outputName=''):
        """
        Clone a given repository. Now it is assumed that is hosted in github.
        If user is None, GITHUB_USER will be used by default.
        """
        user = user or GITHUB_USER
        output = outputName if outputName else os.path.join(outputDir, name)

        if not self.useHttps:
            url = 'git@github.com:%s/%s.git' % (user, name)
        else:
            url = 'https://github.com/%s/%s.git' % (user, name)

        self.system('git clone --branch %s %s %s' % (branch, url, output))

    def installFromSource(self, name, srcSubFolder, branch=None, **kwargs):
        clean = kwargs.get('clean', False)
        outputDir = os.path.join(self.SCIPION_SRC, srcSubFolder)
        branch = branch or DEFAULT_BRANCH
        outputSrcDir = os.path.join(outputDir, name)
        if os.path.exists(outputSrcDir):
            if clean:
                self.removeDir(outputSrcDir)
            else:
                raise Exception("Output source dir '%s' already exists."
                                % outputSrcDir)
        user = kwargs.get('user', None)
        devel = kwargs.get('devel', True)
        self.clone(name, outputDir=outputDir, branch=branch,
                   user=user, devel=devel)
        self.pipInstall(f'-e {outputSrcDir}')

    def createFolders(self):
        for d in [self.SCIPION_HOME,
                  self.SCIPION_SRC,
                  self.SCIPION_TMP,
                  self.SCIPION_CONF]:
            self.createDir(d, clean=True)

    def installConda(self):
        # Download and install miniconda
        # https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh

        # JMRT (2021-09-08) Do not use the last miniconda installer due to
        # the major Python version and the pined versions of pyworkflow's requirements
        #minicondaSh = 'Miniconda3-latest-Linux-x86_64.sh'
        isMac = sys.platform == 'darwin'
        if isMac:
            minicondaSh = 'Miniconda3-py38_4.9.2-MacOSX-x86_64.sh'
        else:
            minicondaSh = 'Miniconda3-py38_4.9.2-Linux-x86_64.sh'

        outputSh = os.path.join(self.SCIPION_TMP, minicondaSh)
        self.system("wget https://repo.continuum.io/miniconda/%s -O %s"
                    % (minicondaSh, outputSh))
        self.system("bash -- %s -b -p %s/conda" % (outputSh, self.SCIPION_HOME))

        # Fix fonts
        if not isMac:
            self.conda('remove tk --force -y')  # remove bad looking tk
            tkFile = 'tk-8.6.10-h14c3975_1005.tar.bz2'
            outputTk = os.path.join(self.SCIPION_TMP, tkFile)
            self.system("wget https://anaconda.org/scipion/tk/8.6.10/download/linux-64/%s -O %s"
                        % (tkFile, outputTk))
            self.condaInstall(outputTk)

        # Install some deps via conda
        self.condaInstall("libtiff=4.1 fftw=3.3.8 hdf5=1.12 openjdk=8 "
                          "numpy=1.19.2 scipy configparser=5.0.0 "
                          "matplotlib=3.2.2 requests=2.25.1 "
                          "pillow=7.1.2 psutil=5.7.0",
                          channel='conda-forge')

        if not isMac:
            self.condaInstall('cudatoolkit=10.1', channel='conda-forge')

        if not self.buildXmipp:
            # If we are not building xmipp, we can already install openmpi from the conda channel
            self.condaInstall("openmpi=4.0.4 mpi4py", channel='conda-forge')

        # Install some required deps via pip
        self.pipInstall('scons mrcfile empiar_depositor pathlib2 poster3 jsonschema bibtexparser==1.2.0')

    def installCore(self):
        self.installFromSource('scipion-pyworkflow', 'core', clean=True)
        self.installFromSource('scipion-em', 'core', clean=True)
        self.installFromSource('scipion-app', 'core', clean=True)

    def installPlugins(self):
        for plugin in self.PLUGINS_LIST:
            self.installFromSource(plugin, 'plugins', clean=True)

        # Xmipp plugin is special since it is located at I2PC
        self.installFromSource('scipion-em-xmipp', 'plugins',
                               branch=XMIPP_BRANCH, clean=True,
                               user=XMIPP_USER)

    def createConfig(self):
        files = os.path.join(here, 'files')
        # print("Copying config files from: ", files)
        self.system('cp %s/scipion.bashrc %s/' % (files, self.SCIPION_HOME))
        self.system('cp %s/*.conf %s/' % (files, self.SCIPION_CONF))
        self.system('cp %s/update.py %s/' % (files, self.SCIPION_HOME))

    # ------ Either build Xmipp or install binaries -----------------------
    def buildXmipp(self):
        self.clone('xmipp', branch=XMIPP_BRANCH, user=XMIPP_USER,
                   outputName=self.XMIPP_BUNDLE)

        xmippInstallScript = os.path.join(self.XMIPP_BUNDLE, 'install_xmipp.sh')
        with open(xmippInstallScript, 'w') as f:
            f.write("""
            %s && cd %s && python --version

            echo "\n>>> ./xmipp get_devel_sources"
            ./xmipp get_devel_sources %s

            echo "\n>>> ./xmipp config noAsk"
            ./xmipp config noAsk

            echo "\n>>> ./xmipp get_dependencies"
            ./xmipp get_dependencies

            echo "\n>>> python ./xmipp compile"
            python ./xmipp compile %d
            python ./xmipp install
            """ % (self.ENV_ACTIVATE, self.XMIPP_BUNDLE, XMIPP_BRANCH, J))

        self.system('bash -ex %s' % xmippInstallScript)

    def installXmipp(self, build=False):
        self.createDir(self.XMIPP_BUNDLE, clean=True)

        if build:
            self.buildXmipp()
            # Install openmpi now, to not interfere with Xmipp compilation
            self.condaInstall("openmpi=4.0.4", channel='conda-forge')
        else:
            xmippBin = 'xmipp-v3.20.07.tgz'
            self.system('cd %s; '
                      'wget https://github.com/delarosatrevin/scipion-install-bin/raw/master/%s; '
                      'tar -xzf %s' % (self.XMIPP_BUNDLE, xmippBin, xmippBin))


def get_parser():
    """ Return the argparse parser, so we can get the arguments """

    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut

    add('installFolder', metavar='INSTALL_FOLDER',
        help='Installation folder.')
    add('--https', action='store_true',
        help='Use https URL to retrieve repositories')
    add('--only_print', action='store_true',
        help='Only print installation commands')
    add('--only_xmipp', action='store_true',
        help='Only install Xmipp. ')
    add('--build_xmipp', action='store_true',
        help='Build Xmipp (usually to generate a binary)')
    add('--skip_xmipp', action='store_true',
        help='Install Scipion without Xmipp (useful for Mac)')
    add('--skip_plugins', action='store_true',
        help="Do not install the plugins, just core ones. ")

    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    si = ScipionInstaller(args.installFolder,
                          useHttps=args.https)

    if not args.only_xmipp:
        si.createFolders()
        si.installConda()
        si.installCore()
        if not args.skip_plugins:
            si.installPlugins()
        si.createConfig()

    if not args.skip_xmipp:
        si.installXmipp(args.build_xmipp)

    cmdStr = '\n'.join(si.commands)

    if args.only_print:
        print(cmdStr)
    else:
        installScript = os.path.join(here, 'install_script.sh')

        with open(installScript, 'w') as f:
            f.write(f'printenv\n{cmdStr}\n')

        env = {}
        for k, v in os.environ.items():
            if k.startswith('CONDA'):
                continue
            env[k] = v

        subprocess.run(['bash', '-ex', installScript], env=env)



