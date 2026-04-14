#### to run : source analyse.sh

#Run dataframe analysis on locally generated files
analysis_config=${FCCANACONFS}
analysis_script=analysis_stage1.py

detector=IDEA

# input files (from Pythia+Delphes)
path=/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/${detector}

# output path
outputpath=/eos/user/g/gmarchio/fcc/analysis/selection/ZvvHqq-365/${campaign}/${detector}/analysis-stage1/test/
# outputpath=.

for process in \
    wzp6_ee_nunuH_Hbb_ecm365 \
    #wzp6_ee_nunuH_Hcc_ecm365 \
    #wzp6_ee_nunuH_Hss_ecm365 \
    #wzp6_ee_nunuH_Hgg_ecm365 \
    #wzp6_ee_nunuH_Htautau_ecm365 \
    #wzp6_ee_nunuH_HZZ_ecm365 \
    #wzp6_ee_nunuH_HWW_ecm365 	
do
    echo "Running over files in $path/$process"
# everything
#    fccanalysis run $analysis --output ${outputpath}/${process}/events_all.root --files-list ${path}/${process}/events_*.root
# debug 1000 events
    fccanalysis run $analysis_config/$analysis_script --output ${outputpath}/${process}/events_all.root --files-list ${path}/${process}/events_*.root  --nevents 1000
# debug 1 file (test MT)
    # files=`ls $path/$process/*.root | head -1`
    # fccanalysis run $analysis_config/$analysis_script --output ${outputpath}/${process}/events_all.root --files-list ${files}    
    #
    echo ""
done
