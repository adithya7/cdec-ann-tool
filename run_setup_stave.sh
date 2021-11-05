#!/bin/bash

eval "$(conda shell.bash hook)"

cd multidoc-stave

# setup conda environment
conda create -q -y -n multidoc-stave python=3.7
conda activate multidoc-stave

# install Django, numpy
python -m pip install -r requirements.txt

# read package.json and install necessary packages for ReactJS frontend
npm install
# you might have to run `npm audit fix`
npm audit fix

mkdir simple-backend/frontend

npm run-script build
cp -r build simple-backend/frontend

cd ..