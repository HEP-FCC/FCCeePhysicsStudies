# Initial setup
cd analysis
git clone git@github.com:giovannimarchiori/FCCAnalyses.git
cd FCCAnalyses
git checkout gmarchio-main-20240301
cd ..

git clone git@github.com:giovannimarchiori/FCCeePhysicsPerformance.git
cd FCCeePhysicsPerformance
git checkout gmarchio-main-20240301
cd ..

cp FCCeePhysicsPerformance/case-studies/higgs/hcc/analysis/ZllHqq/FCCAnalyses.PDG.patch .
git apply FCCAnalyses.PDG.patch
rm FCCAnalyses.PDG.patch

# go to work directory and setup environment (do it every time)
cd FCCeePhysicsPerformance/case-studies/higgs/hcc/analysis/ZvvHqq-365
source start.sh

# compile FCCAnalyses package 1st time - and any time you edit code inside it
source compile.sh

