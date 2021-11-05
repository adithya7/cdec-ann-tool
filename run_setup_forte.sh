#!/bin/bash

eval "$(conda shell.bash hook)"

cd multidoc-forte

# setup conda environment
conda create -q -y -n multidoc-forte python=3.7
conda activate multidoc-forte

# install forte library
git clone https://github.com/asyml/forte.git
cd forte
# our annotation toolkit is tested on this version of forte
git checkout a75aa09eb7a60f442b16ca57a2619d321001efba
python -m pip install .
cd ..

# install allennlp, allennlp-models, numpy
python -m pip install -r requirements.txt

# Download NER models
cd ner
python download_models.py
cd ..

# Generate the ontology using event_ontology.json as input (provided), and current directory . as output path.
# This should output a folder named `edu` and file `full.json`. The file `full.json` contains the ontology needed for the visualization UI.
# To fully understand the generation code, check https://asyml-forte.readthedocs.io/en/latest/ontology_generation.html
generate_ontology create -i event_ontology.json -o . -m full.json -r

cd ..