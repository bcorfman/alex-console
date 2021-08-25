#!/bin/bash
source "$CONDA_PREFIX/etc/profile.d/conda.sh"
conda deactivate
conda env remove -n alex
