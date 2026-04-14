os=`cat /etc/os-release | grep ^ID= | awk -F '"' '{print $2}'`
if [[ "$os" == "rocky" ]]; then
    echo "OS is rocky"
    source setup_rocky.sh
    export FCCANAOUTPUT=$PWD/../../../../../../output/ZvvHqq-365/
else
    export FCCANAOUTPUT=/eos/user/g/gmarchio/fcc/analysis/selection/ZvvHqq-365/
fi
export FCCANALYSES=$PWD/../../../../../../FCCAnalyses
export FCCANALYSIS=$PWD
export FCCANACONFS=$PWD/../../FCCAnalyses-config/ZvvHqq-365
cwd=$PWD
cd $FCCANALYSES
source setup.sh
cd $cwd
export FCCANALYSES=$PWD/../../../../../../FCCAnalyses
