#!/bin/bash

export repo='/afs/cern.ch/user/a/aumarten/work/fcc'

echo "-----------------------------------------------------------------------------------------------------------------------"
source $repo/setup.sh
echo "Software stack loaded, start analysis"
echo "-----------------------------------------------------------------------------------------------------------------------"

fccanalysis run $repo/my3pipi0_reco_public_sample.py
if [[ $status -eq 0 ]]; then
    echo "Success"
else
    echo "Error (Exit-Code $status)"
fi
