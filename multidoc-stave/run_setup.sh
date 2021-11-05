#!/bin/bash

conda create -q -y -n multidoc-stave python=3.7
conda activate multidoc-stave

# install Django
python -m pip install Django

# read package.json and install necessary packages for ReactJS frontend
npm install
# you might have to run `npm audit fix`

mkdir simple-backend/frontend

npm run-script build
cp -r build simple-backend/frontend

cd simple-backend
python manage.py runserver 0.0.0.0:8004