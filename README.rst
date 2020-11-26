
scipion-install
===============

Utility repository to help installing Scipion from scratch, either using Xmipp pre-compiled binaries or builing it from source.


Installing Scipion
------------------

The main goal of this tools is to install Scipion as simple as possible.
It should not required any admin privileges in your computer neither compiler tools.

.. code-block:: bash

    git clone https://github.com/delarosatrevin/scipion-install.git
    cd scipion-install 
    python ./install.py SCIPION_FOLDER --https
    
After this you should have a basic Scipion 3.0 installation in SCIPION_FOLDER.
You can load Scipion environment by: 

.. code-block:: bash

    . SCIPION_FOLDER/scipion.bashrc 
    
Then you can install some binaries to work with:

.. code-block:: bash

    scipion installb cistem cryolo cryolo_model ctffind4 gctf motioncor2
    
It is recommended that you install Relion 3.1 separately and then link it in the EM folder:

.. code-block:: bash

    cd SCIPION_FOLDER/EM
    ln -s RELION_3.1_FOLDER relion-3.1.0
    
And then run some tests to validate the installation:

.. code-block:: bash

    scipion test [UPDATE]
    
    
 
Development installation
------------------------

A development installation is very similar that the previous one, since it install the plugins from the source code.
Just avoid the **--https** option if you want to be able to commit changes to the source code repositories.


Building Xmipp binaries
-----------------------

You should not need to worry about this section, it is more a note to myself.
I build the Xmipp binaries in my Ubuntu 18.04.4 workstation with some specific modules versions.

.. code-block:: bash

    module load cuda/10.1.2 gcc/8.1 openmpi/4.0.4
    python ./install.py SCIPION_FOLDER --build-xmipp
    
Then I just create a tar file with the Xmipp build directory and commit it to the scipion-install-bin repo:

.. code-block:: bash

    cd SCIPION_FOLDER/source/xmipp-bundle
    tar -cvzf xmipp-v3.20.07.tgz build
    mv xmipp-v3.20.07.tgz  ~work/development/scipion/scipion-install-bin/
    cd ~work/development/scipion/scipion-install-bin/
    git add xmipp-v3.20.07.tgz
    git commit -m "New Xmipp binary file" 
    
  

 


