#!/bin/bash
source "$CONDA_PREFIX/etc/profile.d/conda.sh"
conda update -y -n base -c defaults conda
conda create -y -n alex python=3.9.*
conda activate alex
pip install -r ./tests/requirements.txt
pip install -r requirements.txt
