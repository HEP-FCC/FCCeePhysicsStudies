#!/bin/bash

#export repo='/afs/cern.ch/user/a/aumarten/work/fcc'
export repo='/eos/user/a/aumarten/fcc-tau'
echo "-----------------------------------------------------------------------------------------------------------------------"
source $repo/setup.sh
echo "Software stack loaded, start analysis"
echo "-----------------------------------------------------------------------------------------------------------------------"

fccanalysis run $repo/my3pi_reco_public_sample.py
if [[ $status -eq 0 ]]; then
    echo "Success"
else
    echo "Error (Exit-Code $status)"
fi
