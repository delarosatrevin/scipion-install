# This script is valid for bash and zsh

export XMIPP_HOME=$SCIPION_HOME/source/xmipp-bundle/build
export XMIPP_SRC=/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/src
export PATH=/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/build/bin:$PATH
export LD_LIBRARY_PATH=/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/build/lib:/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/build/bindings/python:::$LD_LIBRARY_PATH
export PYTHONPATH=/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/build/bindings/python:/home/josem/work/development/testing-scipion-install/scipion3/source/xmipp-bundle/build/pylib:$PYTHONPATH

alias x='xmipp'
alias xsj='xmipp_showj'
alias xio='xmipp_image_operate'
alias xis='xmipp_image_statistics'
alias xih='xmipp_image_header'
alias xmu='xmipp_metadata_utilities'
