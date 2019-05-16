#!/usr/bin/bash

ABS="$( realpath ${BASH_SOURCE[0]})"
DIR="$( dirname $ABS)"

export SCIPION_ROOT=$DIR
export SCIPION_HOME=$SCIPION_ROOT/v2.0.0

export SCIPION_SW=$SCIPION_ROOT/SW
export SCIPION_EM=$SCIPION_ROOT/EM

export SCIPION_PLUGINS=$SCIPION_ROOT/plugins

# Add all plugins to PYTHONPATH
# in a future we might want to install them properly
for f in $SCIPION_PLUGINS/scipion-em-*
do
    export PYTHONPATH=$PYTHONPATH:$f    
done

alias scipion='$SCIPION_HOME/scipion --config $SCIPION_HOME/config/scipion.conf'
alias spy='scipion python'

export XMIPP_HOME=$SCIPION_EM/xmipp
export XMIPP_SRC=$XMIPP_HOME/src
export PATH=$SCIPION_SW/bin:$XMIPP_HOME/bin:$PATH
export LD_LIBRARY_PATH=$SCIPION_SW/lib:$XMIPP_HOME/lib:$XMIPP_HOME/bindings/python:$LD_LIBRARY_PATH
export PYTHONPATH=$XMIPP_HOME/bindings/python:$XMIPP_HOME/pylib:$PYTHONPATH

alias x='xmipp'
alias xsj='xmipp_showj'
alias xio='xmipp_image_operate'
alias xis='xmipp_image_statistics'
alias xih='xmipp_image_header'
alias xmu='xmipp_metadata_utilities'


