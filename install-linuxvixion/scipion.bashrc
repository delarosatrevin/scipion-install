#!/usr/bin/bash

ABS="$( realpath ${BASH_SOURCE[0]})"
DIR="$( dirname $ABS)"

export SCIPION_ROOT=$DIR
export SCIPION_HOME=$SCIPION_ROOT

export SCIPION_SW=$SCIPION_ROOT/conda
export SCIPION_EM=$SCIPION_ROOT/EM
export SCIPION_CONFIG=$SCIPION_HOME/config/scipion.conf

# Needed by some plugins
export EM_ROOT=$SCIPION_EM

export SCIPION_PLUGINS=$SCIPION_ROOT/source/plugins

# Activate the environment
export PATH=$SCIPION_SW/bin:$PATH
export LD_LIBRARY_PATH=$SCIPION_SW/lib:$LD_LIBRARY_PATH

# Setup Xmipp
export XMIPP_HOME=$SCIPION_HOME/source/xmipp-bundle/build
export PATH=$XMIPP_HOME/bin:$PATH
export LD_LIBRARY_PATH=$XMIPP_HOME/lib:$XMIPP_HOME/bindings/python:$LD_LIBRARY_PATH
export PYTHONPATH=$XMIPP_HOME/bindings/python:$XMIPP_HOME/pylib:$PYTHONPATH

alias x='xmipp'
alias xsj='xmipp_showj'
alias xio='xmipp_image_operate'
alias xis='xmipp_image_statistics'
alias xih='xmipp_image_header'
alias xmu='xmipp_metadata_utilities'

alias scipion='scipion --config $SCIPION_CONFIG'
alias update_scipion3='python $SCIPION_HOME/update.py'


