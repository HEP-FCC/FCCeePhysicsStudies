# import common definitions
import os, sys
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_config import *

import ROOT

# global parameters
showFirstGen = False
showFV = False
inputDir = basedir  + '/analysis-final/hists/'
outdir = inputDir.replace('hists', 'plots')
intLumi = lumiRef*1e3 # reference lumi in 1/pb
ana_tex = 'e^{+}e^{-} #rightarrow ZH #rightarrow #nu#bar{#nu} + X'
delphesVersion = '3.4.2'
energy = 240.0
collider = 'FCC-ee'
BES = False
formats = ['pdf']
yaxis = ['lin']
stacksig = ['stack', 'nostack']
fillsig = False
scaleSig = 1.0
xleg = 0.67

# Plots signal (resp. background) ordered by their yield
yieldOrder = True

# variables = ['missing_e', 'dijets_mass', 'higgs_hadronic_recoil_mass', "jet1_npart", "jet2_npart", "dijets_cos_theta", 'jets_d23', 'dijets_mass_bb']
variables = ['mvis', 'mvis_zoom', 'higgs_hadronic_recoil_mass_zoom']

# Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis.
# The name of the selections should be the same than in the final selection
# Use cuts defined in analysis_config
selections = {}
# do plot for all selection steps
# selections['ZH'] = sel
# override, do only for 1st and last tep
selections['ZH'] = ['selNone', 'sel_dmergeok']

# these could be moved to analysis config
extralabel = {}
extralabel['selNone'] = 'No selection'
## extralable['selNone'] = 'No selection'
## extralabel['sel_mvis_mmiss'] = 'Final selection'
extralabel['sel_dmergeok'] = 'Final selection'

colors = {}
palette = {}
icolor=2000
for process, colorname in processColors.items():
    color = colordict[colorname]
    r = int(color[1:3],16)
    g = int(color[4:6],16)
    b = int(color[5:8],16)
    palette[process] = ROOT.TColor(icolor,r/255.,g/255.,b/255.,colorname)
    colors[process] = icolor
    icolor+=1
    
plots = {}

plots['ZH'] = {
    'signal': {
        'ZHbb': ['wzp6_ee_nunuH_Hbb_ecm240'],
        'ZHgg': ['wzp6_ee_nunuH_Hgg_ecm240'],
        'ZHcc': ['wzp6_ee_nunuH_Hcc_ecm240'],
        'ZHss': ['wzp6_ee_nunuH_Hss_ecm240'],
        'ZHtautau': ['wzp6_ee_nunuH_Htautau_ecm240'],
        'ZHWW': ['wzp6_ee_nunuH_HWW_ecm240'],
        'ZHZZ': ['wzp6_ee_nunuH_HZZ_ecm240'],
    },
    'backgrounds': {
        'WW': ['p8_ee_WW_ecm240'],
        'ZZ': ['p8_ee_ZZ_ecm240'],
        'Zqq': ['p8_ee_Zqq_ecm240'],
        'nuenueZ' : ['wzp6_ee_nuenueZ_ecm240'],
        'qqH':
        [
            'wzp6_ee_qqH_Hbb_ecm240',
            'wzp6_ee_qqH_Hcc_ecm240',
            'wzp6_ee_qqH_Hgg_ecm240',
            'wzp6_ee_qqH_Hss_ecm240',
            'wzp6_ee_qqH_HWW_ecm240',
            'wzp6_ee_qqH_HZZ_ecm240',
            'wzp6_ee_qqH_Htautau_ecm240',
            'wzp6_ee_ssH_Hbb_ecm240',
            'wzp6_ee_ssH_Hcc_ecm240',
            'wzp6_ee_ssH_Hgg_ecm240',
            'wzp6_ee_ssH_Hss_ecm240',
            'wzp6_ee_ssH_HWW_ecm240',
            'wzp6_ee_ssH_HZZ_ecm240',
            'wzp6_ee_ssH_Htautau_ecm240',
            'wzp6_ee_ccH_Hbb_ecm240',
            'wzp6_ee_ccH_Hcc_ecm240',
            'wzp6_ee_ccH_Hgg_ecm240',
            'wzp6_ee_ccH_Hss_ecm240',
            'wzp6_ee_ccH_HWW_ecm240',
            'wzp6_ee_ccH_HZZ_ecm240',
            'wzp6_ee_ccH_Htautau_ecm240',
            'wzp6_ee_bbH_Hbb_ecm240',
            'wzp6_ee_bbH_Hcc_ecm240',
            'wzp6_ee_bbH_Hgg_ecm240',
            'wzp6_ee_bbH_Hss_ecm240',
            'wzp6_ee_bbH_HWW_ecm240',
            'wzp6_ee_bbH_HZZ_ecm240',
            'wzp6_ee_bbH_Htautau_ecm240',
        ]
        # 'ZHnonhad': [
        #     'wzp6_ee_nunuH_Htautau_ecm240',
        #     'wzp6_ee_nunuH_HWW_ecm240',
        #     'wzp6_ee_nunuH_HZZ_ecm240',
        # ],

    },
}

if showFirstGen:
    plots['ZH']['signal'].update({
        'ZHuu': ['wzp6_ee_nunuH_Huu_ecm240'],
        'ZHdd': ['wzp6_ee_nunuH_Hdd_ecm240'],
    })

if showFV:
    plots['ZH']['signal'].update({
        'ZHcu': ['wzp6_ee_nunuH_Hcu_ecm240'],
        'ZHbs': ['wzp6_ee_nunuH_Hbs_ecm240'],
        'ZHbd': ['wzp6_ee_nunuH_Hbd_ecm240'],
        'ZHsd': ['wzp6_ee_nunuH_Hsd_ecm240'],
    })
    
legend = {}
for procType in plots['ZH']:
    for proc in plots['ZH'][procType]:
        legend[proc] = processLabels[proc]

# override default legend titles with e.g.
# legend['Zqq'] = 'Z/#gamma*'
