#!/bin/bash

set -e
#
# This script will update the Scipion2 installation for the latest patches.
# It needs to be run as root.

echo "Updating your Scipion2 installation."
echo "It will take approximately 5 minutes to complete."


sleep 4
cd $SCIPION_HOME
git pull --prune
cd ../plugins
git submodule foreach "(git checkout master; git pull --prune)"

echo ""
echo "Update Complete"