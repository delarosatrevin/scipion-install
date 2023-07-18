
scipion-install
===============

Utility script and files to smoothly  install Scipion on Linux/MacOS.

NO COMPILATION REQUIRED!!!

It will download a Miniconda installer and install core plugins and some EM plugins.
It will also ensure compatibility in library versions with previously compiled Xmipp binary.

Additionally, EMHub will be also installed.


Requirements
------------
* **git** to clone install repository and other plugins
* **python** to run the install script


Installing Scipion
------------------

It should be very easy to install Scipion following these steps. Just be patient
for conda to resolve dependencies and environment libraries. Installation should not
require any admin privileges in your computer or compiler tools.

Replace `SCIPION_FOLDER` in the following command with the path where you want to 
install Scipion.

.. code-block:: bash

    git clone https://github.com/delarosatrevin/scipion-install.git
    cd scipion-install 
    python ./install.py SCIPION_FOLDER

After this, you should have a basic Scipion 3.0 installation in SCIPION_FOLDER.
You can load the Scipion environment by: 

.. code-block:: bash

    source SCIPION_FOLDER/bashrc
    
Then you can install some binaries to work with:

.. code-block:: bash

    scipion installb cistem cryolo cryolo_model ctffind4 gctf motioncor2
    
It is recommended that you install Relion separately and then link it in the EM folder:

.. code-block:: bash

    cd SCIPION_FOLDER/EM
    ln -s RELION_4.0_FOLDER relion-4.0
    
And then run some tests to validate the installation:

.. code-block:: bash

    scipion test [UPDATE]
    
    
 
Development installation
------------------------

A development installation is very similar that the previous one, since it install the plugins from the source code.
Just pass **--git_clone ssh* to use that method for cloning from GitHub. The installation command will be:

.. code-block:: bash

    python ./install.py SCIPION_FOLDER --git_clone ssh


Xmipp binaries
--------------

Xmipp binaries used in the installation are pre-built and hosted in the following repository:

https://github.com/delarosatrevin/xmipp-binaries

