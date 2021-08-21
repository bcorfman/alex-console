#!/bin/bash
conda create -n alex python=3.9.*
conda activate alex
pip install -r ./tests/requirements.txt
pip install -r requirements.txt