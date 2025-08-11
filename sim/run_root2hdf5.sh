#!/bin/bash

#root files directory
ROOT_DIR="../data/CLD_FULL/"

#script to run
PYTHON_SCRIPT="read.py"

#loop over file indices
for i in $(seq 1 100); do
    INDEX=$(printf "%03d" $i)
    ROOT_FILE="${ROOT_DIR}gev91ee_zboson_mm_${INDEX}_CLD_RECO_edm4hep.root"
    if [ -f "$ROOT_FILE" ]; then
        echo "Processing $ROOT_FILE"
        python $PYTHON_SCRIPT "$ROOT_FILE"
    else
        echo "Warning: $ROOT_FILE not found. Skipping..."
    fi
done

