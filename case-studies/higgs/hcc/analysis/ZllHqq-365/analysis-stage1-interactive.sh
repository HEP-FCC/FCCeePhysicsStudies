#### to run : source analyse.sh

#Run dataframe analysis on locally generated files
# analysis_config=../../FCCAnalyses-config/ZllHqq-365
analysis_config=${FCCANACONFS}
analysis_script=analysis_stage1.py

campaign=winter2023
detector=IDEA

# input files (from Pythia+Delphes)
# central production
path=/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/${detector}
# private production
# path=/eos/user/g/gmarchio/fcc/generation/DelphesEvents/${campaign}/${detector}

# output path
outputpath=/eos/user/g/gmarchio/fcc/analysis/selection/ZllHqq-365/${campaign}/${detector}/analysis-stage1/test/
# outputpath=.

for process in \
    wzp6_ee_eeH_Hbb_ecm365 \
#    wzp6_ee_mumuH_Hbb_ecm365 \
#    p8_ee_tt_ecm365 \
#    wzp6_ee_eeH_Huu_ecm365 \
#    wzp6_ee_eeH_Hdd_ecm365 \
#    wzp6_ee_mumuH_Huu_ecm365 \
#    wzp6_ee_mumuH_Hdd_ecm365 \
#    wzp6_ee_eeH_Hbs_ecm365 \
#    wzp6_ee_eeH_Hbd_ecm365 \
#    wzp6_ee_eeH_Hsd_ecm365 \
#    wzp6_ee_eeH_Hcu_ecm365 \
#    wzp6_ee_mumuH_Hbs_ecm365 \
#    wzp6_ee_mumuH_Hbd_ecm365 \
#    wzp6_ee_mumuH_Hsd_ecm365 \
#    wzp6_ee_mumuH_Hcu_ecm365 \
#    wzp6_ee_eeH_HZZ_ecm365 
#    wzp6_ee_mumuH_Hgg_ecm365 
#    wzp6_ee_eeH_Hcc_ecm365 \
#    wzp6_ee_eeH_Hgg_ecm365 \
#    wzp6_ee_eeH_Hss_ecm365 \
#    wzp6_ee_eeH_Htautau_ecm365 \
#    wzp6_ee_eeH_HWW_ecm365 
#
#    wzp6_ee_nunuH_Hbb_ecm365 \
#    wzp6_ee_nunuH_Hcc_ecm365 \
#    wzp6_ee_nunuH_Hgg_ecm365 \
#    wzp6_ee_nunuH_Hss_ecm365 \
#    wzp6_ee_nunuH_Huu_ecm365 \
#
#    p8_ee_ZH_Znunu_Hbb_ecm365 \
#    p8_ee_ZH_Znunu_Hcc_ecm365 \
#    p8_ee_ZH_Znunu_Hgg_ecm365 \
#    p8_ee_ZH_Znunu_Hss_ecm365 \
#    p8_ee_ZH_Znunu_Huu_ecm365 \
#
#    wzp6_ee_ZllHqq_ecm365 \
#    wzp6_ee_ZllHtt_ecm365 \
#    wzp6_ee_ZmmHnonhad_ecm365 \
#    wzp6_ee_ZeeHnonhad_ecm365 \
#    wzp6_ee_ZmmHcc_ecm365 \
#    wzp6_ee_ZeeHcc_ecm365 \
#    wzp6_ee_ZmmHgg_ecm365 \
#    wzp6_ee_ZeeHgg_ecm365 \
#    wzp6_ee_ZmmHbb_ecm365 \
#    wzp6_ee_ZeeHbb_ecm365 \
do
    echo "Running over files in $path/$process"
    # everything but nonhad
    mkdir -p ${outputpath}/${process}
    # fccanalysis run $analysis_config/$analysis_script --output ${outputpath}/${process}/events_all.root --files-list ${path}/${process}/events_*.root
# debug 1000 events
    fccanalysis run $analysis_config/$analysis_script --output ${outputpath}/${process}/events_all.root --files-list ${path}/${process}/events_*.root  --nevents 1000
# debug 1 file (test MT)
    # files=`ls $path/$process/*.root | head -1`
    # fccanalysis run $analysis_config/$analysis_script --output ${outputpath}/${process}/events_all.root --files-list ${files}    
    #
    echo ""
done
