debug = False

# import common definitions
import os, sys
configdir = os.getenv('FCCANACONFS')
#if configdir == '':
#    configdir = '../../../FCCAnalyses-config/%s/' % analysis
print('Config directory: ', configdir)
if not os.path.isdir(configdir):
    print('Config directory not found')
    exit(1)
sys.path.append(configdir)
from analysis_config import *


# MC production to run on (SET IN ANALYSIS_CONFIG)
# production = 'winter2023'
# detector = 'IDEA'


# name/tag of the physics analysis (SET IN ANALYSIS_CONFIG, DO NOT MODIFY)
# analysis = 'ZllHqq-365'
# analysis = os.path.split(os.getcwd())[0].split('/')[-1]


# input and output directories (SET AUTOMATICALLY, DO NOT MODIFY)
# central production
indir = '/eos/experiment/fcc/ee/generation/DelphesEvents/'+production+'/'+detector+'/'
# private production
# indir = '/eos/user/g/gmarchio/fcc/generation/DelphesEvents/'+production+'/'+detector+'/'
outdir = basedir + '/analysis-stage1/'
print('Input directory: ', indir)
if not os.path.isdir(indir):
    print('Input directory not found')
    exit(1)
print('Output location: ', outdir)


# analysis script (SET AUTOMATICALLY, DO NOT MODIFY)
script = '%s/analysis_stage1.py' % configdir
print('Analysis script: ' , script)
if not os.path.isfile(script):
    print('Script not found')
    exit(1)


# run nev_per_job = -1 to run on all event in input root files
# TRY LONGLUNCH IF JOBS DO NOT START
# queue = 'longlunch'
queue = 'workday'
# queue = 'espresso'
# nev_per_job = 100
nev_per_job = -1
print('Condor queue: ', queue)
print('Condor events per job: ', nev_per_job)


# list of samples to run on (TODO: take from analysis_config)
samples = []

if analysis == 'ZllHqq-365':
    samples = [
        # Z(ll)H
        'wzp6_ee_eeH_Hbb_ecm365',
        'wzp6_ee_eeH_Hcc_ecm365',
        'wzp6_ee_eeH_Hss_ecm365',
        'wzp6_ee_eeH_Hgg_ecm365',
        'wzp6_ee_eeH_Htautau_ecm365',
        'wzp6_ee_eeH_HWW_ecm365',
        'wzp6_ee_eeH_HZZ_ecm365',
        'wzp6_ee_eeH_Huu_ecm365',
        'wzp6_ee_eeH_Hdd_ecm365',
        'wzp6_ee_eeH_Hbs_ecm365',
        'wzp6_ee_eeH_Hbd_ecm365',
        'wzp6_ee_eeH_Hsd_ecm365',
        'wzp6_ee_eeH_Hcu_ecm365',
        'wzp6_ee_mumuH_Hbb_ecm365',
        'wzp6_ee_mumuH_Hcc_ecm365',
        'wzp6_ee_mumuH_Hss_ecm365',
        'wzp6_ee_mumuH_Hgg_ecm365',
        'wzp6_ee_mumuH_Htautau_ecm365',
        'wzp6_ee_mumuH_HWW_ecm365',
        'wzp6_ee_mumuH_HZZ_ecm365',
        'wzp6_ee_mumuH_Huu_ecm365',
        'wzp6_ee_mumuH_Hdd_ecm365',
        'wzp6_ee_mumuH_Hbs_ecm365',
        'wzp6_ee_mumuH_Hbd_ecm365',
        'wzp6_ee_mumuH_Hsd_ecm365',
        'wzp6_ee_mumuH_Hcu_ecm365',
    ]
    samples.extend([
        # bkg
        'p8_ee_WW_ecm365',
        'p8_ee_ZZ_ecm365',
        'p8_ee_Zqq_ecm365',
        'p8_ee_tt_ecm365',
        'wzp6_ee_mumu_ecm365',
        'wzp6_ee_ee_Mee_30_150_ecm365'
        ])
elif analysis == 'ZvvHqq-365':
    samples = [
        # Z(nunu)H
        'wzp6_ee_nunuH_Hbb_ecm365',
        'wzp6_ee_nunuH_Hcc_ecm365',
        'wzp6_ee_nunuH_Hss_ecm365',
        'wzp6_ee_nunuH_Hgg_ecm365',
        'wzp6_ee_nunuH_Htautau_ecm365',
        'wzp6_ee_nunuH_HWW_ecm365',
        'wzp6_ee_nunuH_HZZ_ecm365',
        'wzp6_ee_nunuH_Huu_ecm365',
        'wzp6_ee_nunuH_Hdd_ecm365',
        'wzp6_ee_nunuH_Hbs_ecm365',
        'wzp6_ee_nunuH_Hbd_ecm365',
        'wzp6_ee_nunuH_Hsd_ecm365',
        'wzp6_ee_nunuH_Hcu_ecm365',
        # Z(bb)H
        'wzp6_ee_bbH_Hbb_ecm365',
        'wzp6_ee_bbH_Hcc_ecm365',
        'wzp6_ee_bbH_Hss_ecm365',
        'wzp6_ee_bbH_Hgg_ecm365',
        'wzp6_ee_bbH_Htautau_ecm365',
        'wzp6_ee_bbH_HWW_ecm365',
        'wzp6_ee_bbH_HZZ_ecm365',
        # Z(cc)H
        'wzp6_ee_ccH_Hbb_ecm365',
        'wzp6_ee_ccH_Hcc_ecm365',
        'wzp6_ee_ccH_Hss_ecm365',
        'wzp6_ee_ccH_Hgg_ecm365',
        'wzp6_ee_ccH_Htautau_ecm365',
        'wzp6_ee_ccH_HWW_ecm365',
        'wzp6_ee_ccH_HZZ_ecm365',
        # Z(ss)H
        'wzp6_ee_ssH_Hbb_ecm365',
        'wzp6_ee_ssH_Hcc_ecm365',
        'wzp6_ee_ssH_Hss_ecm365',
        'wzp6_ee_ssH_Hgg_ecm365',
        'wzp6_ee_ssH_Htautau_ecm365',
        'wzp6_ee_ssH_HWW_ecm365',
        'wzp6_ee_ssH_HZZ_ecm365',
        # Z(qq)H
        'wzp6_ee_qqH_Hbb_ecm365',
        'wzp6_ee_qqH_Hcc_ecm365',
        'wzp6_ee_qqH_Hss_ecm365',
        'wzp6_ee_qqH_Hgg_ecm365',
        'wzp6_ee_qqH_Htautau_ecm365',
        'wzp6_ee_qqH_HWW_ecm365',
        'wzp6_ee_qqH_HZZ_ecm365',
    ]
    samples.extend([
        # bkg
        'p8_ee_WW_ecm365',
        'p8_ee_ZZ_ecm365',
        'p8_ee_Zqq_ecm365',
        'p8_ee_tt_ecm365',
        'wzp6_ee_nuenueZ_ecm365'
        #'wzp6_ee_mumu_ecm365',
        #'wzp6_ee_ee_Mee_30_150_ecm365'    
    ])
# samples=[
#    'wzp6_ee_eeH_Huu_ecm365',
#    'wzp6_ee_eeH_Hdd_ecm365',
#    'wzp6_ee_mumuH_Huu_ecm365',
#    'wzp6_ee_mumuH_Hdd_ecm365',
#    'wzp6_ee_eeH_Hbs_ecm365',
#    'wzp6_ee_eeH_Hbd_ecm365',
#    'wzp6_ee_eeH_Hsd_ecm365',
#    'wzp6_ee_eeH_Hcu_ecm365',
#    'wzp6_ee_mumuH_Hbs_ecm365',
#    'wzp6_ee_mumuH_Hbd_ecm365',
#    'wzp6_ee_mumuH_Hsd_ecm365',
#    'wzp6_ee_mumuH_Hcu_ecm365',
#    ]
from datetime import datetime
now = datetime.now()
string = now.strftime('%Y-%m-%d-%H:%M:%S')
logfile = 'condor-sub-%s.txt' %string

outf = open(logfile, 'w')
outf.write('Analysis name: %s\n' % analysis)
outf.write('Input location: %s\n' % indir)
outf.write('Output location: %s\n' % outdir)
outf.write('Config directory: %s\n' % configdir)
outf.write('Analysis script: %s\n' % script)
outf.write('Condor queue: %s\n' % queue)
outf.write('Condor events per job: %s\n\n' % nev_per_job)


### run condor jobs
# os.system('rm -rf std/*')
os.makedirs("std", exist_ok = True)
for s in samples:
    print('')
    cmd = 'python submitAnalysisJobs.py --indir {}/{} '.format(indir, s)
    cmd += '--outdir {}/{} '.format(outdir, s)
    cmd += '--queue {} --script {} --nev {} '.format(queue, script, nev_per_job)
    if debug:
        cmd += '--dry'
    print(cmd)
    outf.write(cmd)
    outf.write('\n')
    os.system(cmd)
