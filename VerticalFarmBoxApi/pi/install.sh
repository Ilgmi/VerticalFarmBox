#!/bin/bash

if [ $# -eq 0 ]; then
  DATA_DIR=$(pwd)
else
  DATA_DIR="$1"
fi

# Install required packages
sudo apt-get install -y python3;
sudo apt-get install -y python3-pip;
python3 -m pip install -r requirements.txt


echo -e "Files downloaded to ${DATA_DIR}"
