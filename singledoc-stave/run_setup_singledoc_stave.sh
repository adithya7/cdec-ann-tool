#!/bin/bash

eval "$(conda shell.bash hook)"

# setup conda environment
conda create -q -y -n singledoc-stave python=3.7
conda activate singledoc-stave

# setup single-document stave tool
git clone https://github.com/asyml/stave.git
cd stave
# tested compatibility with this version
git checkout adb5d3d2cfd2ab636ce1676151dcb923424b17a1

# install django, django-guardian
pip install -r simple-backend/requirements.txt