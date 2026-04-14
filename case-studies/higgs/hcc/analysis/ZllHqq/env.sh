os=`cat /etc/os-release | grep ^ID= | awk -F '"' '{print $2}'`
if [[ "$os" == "rocky" ]]; then
    export FCCANAOUTPUT=$PWD/../../../../../../output/ZllHqq/
else
    export FCCANAOUTPUT=/eos/user/g/gmarchio/fcc/analysis/selection/ZllHqq/
fi

export FCCANALYSESPKG=$PWD/../../../../../../FCCAnalyses
export FCCANALYSIS=$PWD
export FCCANACONFS=$PWD/../../FCCAnalyses-config/ZllHqq

