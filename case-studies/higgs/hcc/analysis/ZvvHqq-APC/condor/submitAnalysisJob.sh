#!/bin/bash
# source /cvmfs/sw.hsf.org/key4hep/setup.sh
LOCAL_DIR=${1}
SCRIPT=${2}
INPUTFILE=${3}
OUTPUTFILE=${4}
NEVENTS=${5}

echo "LOCAL_DIR dir: ${LOCAL_DIR}"
SCRIPT_DIR="$(dirname "${SCRIPT}")"
echo "SCRIPT_DIR dir: ${SCRIPT_DIR}"
export FCCANACONFS=${SCRIPT_DIR}

cd ${LOCAL_DIR}
source setup.sh
export PYTHONPATH=$LOCAL_DIR:$PYTHONPATH
export LD_LIBRARY_PATH=$LOCAL_DIR/install/lib:$LD_LIBRARY_PATH
#echo "PYTHONPATH: ${PYTHONPATH}"
#echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}"
export ROOT_INCLUDE_PATH=$LOCAL_DIR/install/include/FCCAnalyses:$ROOT_INCLUDE_PATH
export EOS_MGM_URL="root://eospublic.cern.ch"

cd -
mkdir job
cd job

echo "copying file here ... "
python /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py ${INPUTFILE} in.root
ls -l in.root

BASEOUTDIR=$(dirname -- "$OUTPUTFILE")
mkdir -p ${BASEOUTDIR}
echo "output dir:  ${BASEOUTDIR}"
echo "output file:  ${OUTPUTFILE}"

echo "running script ... "
fccanalysis run ${SCRIPT} --output out.root --files-list ./in.root --nevents ${NEVENTS}
echo "job done ... "
python /afs/cern.ch/work/f/fccsw/public/FCCutils/eoscopy.py out.root ${OUTPUTFILE}
echo "copying output ... "
