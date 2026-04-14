os=`cat /etc/os-release | grep ^ID= | awk -F '"' '{print $2}'`
if [[ "$os" == "rocky" ]]; then
    echo "OS is rocky"
    source setup_rocky.sh
    export FCCANAOUTPUT=$PWD/../../../../../../output/ZvvHqq-APC
fi
export FCCANALYSES=$PWD/../../../../../../FCCAnalyses
export FCCANALYSIS=$PWD
export FCCANACONFS=$PWD/../../FCCAnalyses-config/ZvvHqq-APC
cwd=$PWD
cd $FCCANALYSES
echo "Setting up the nightly. If the code does not work, try setting up an older nightly e.g."
echo "source setup.sh -r 2024-04-12"
source setup.sh
cd $cwd
