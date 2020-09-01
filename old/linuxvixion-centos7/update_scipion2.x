#!/bin/bash

set -e
#
#This script will update the LinuxVixion, S.L. Scipion2 installation for the latest patches. It needs to be run as root.

echo "Updating your LinuxVixion, S.L. Certified Scipion2 installation."
echo "It will take approximately 5 minutes to complete."

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

sleep 4
cd $SCIPION_HOME
git pull --prune
cd ../plugins
git submodule foreach "(git checkout master; git pull --prune)"

echo ""
echo "Update Complete"