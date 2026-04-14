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
intLumi = lumiRef*1e3  # in pb-1
ana_tex = 'e^{+}e^{-} #rightarrow ZH #rightarrow l^{+}l^{-} + X'
delphesVersion = '3.4.2'
energy = sqrts
collider = 'FCC-ee'
BES = False
formats = ['pdf']
yaxis = ['lin']
stacksig = ['stack', 'nostack']
fillsig = False
# scaleSig = 1.0
xleg = 0.67

# Plots signal (resp. background) ordered by their yield
yieldOrder = True

# variables = [
#     'zed_flavour',
#     'all_leptons_p',
#     'zed_leptons_p',
#     'extraleptons_p',
#     'N_extra_leptons',
#     'all_jets_p',
#     'jets_p',
#     'N_jets',
#     'cos_theta_Z',
#     'missing_e',
#     'dilepton_mass',
#     'dilepton_mass_2',
#     'dilepton_charge',
#     'hadronic_mass',
#     'hadronic_mass_2',
#     'hadronic_mass_zoom',
#     'm_recoil',
#     'm_recoil_2',
# ]
variables = [ 'm_recoil', 'm_recoil_2' ]

# Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis.
# The name of the selections should be the same than in the final selection
# Use cuts defined in analysis_config
selections = {}
selections['ZH'] = sel

# these could be moved to analysis config
extralabel = {}
extralabel['selNone'] = 'No selection'
extralabel['sel_lep'] = '>0 iso leptons (p>40 GeV)'
extralabel['sel_Z'] = '1 Z(ll) candidate (2 SFOS l, 13<p_{l}<160GeV)'
extralabel['sel_mZ'] = '81<m_{ll}<101 GeV'
extralabel['sel_cosThetaZ'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8'
extralabel['sel_mrecoil'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<200 GeV'
extralabel['sel_mjj'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<200 GeV, 100<m_{jets}<140 GeV'
extralabel['sel_emiss'] = '81<m_{ll}<101 GeV, |cos#theta_{ll}|<0.8, 120<m_{recoil}<200 GeV, 100<m_{jets}<140 GeV, E_{miss}<30 GeV'
extralabel['sel_ej2'] = 'E_{j2}>15 GeV'
extralabel['sel_leptonveto'] = 'Z(ll), m_{ll}, |cos#theta_{ll}|, m_{recoil}, m_{jets}, E_{miss}, lep. veto'
extralabel['sel_dmergeok'] = 'Z(ll), m_{ll}, |cos#theta_{ll}|, m_{recoil}, m_{jets}, E_{miss}, lep. veto, d_{ij}>0'
extralabel['finalsel'] = 'Z(ll), m_{ll}, |cos#theta_{ll}|, m_{recoil}, m_{jets}, E_{miss}, lep. veto'

palette = {}
colors = {}
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
        'ZHbb': ['wzp6_ee_eeH_Hbb_ecm365', 'wzp6_ee_mumuH_Hbb_ecm365'],
        'ZHgg': ['wzp6_ee_eeH_Hgg_ecm365', 'wzp6_ee_mumuH_Hgg_ecm365'],
        'ZHcc': ['wzp6_ee_eeH_Hcc_ecm365', 'wzp6_ee_mumuH_Hcc_ecm365'],
        'ZHss': ['wzp6_ee_eeH_Hss_ecm365', 'wzp6_ee_mumuH_Hss_ecm365'],
        'ZHtautau': ['wzp6_ee_eeH_Htautau_ecm365', 'wzp6_ee_mumuH_Htautau_ecm365'],
        'ZHWW': ['wzp6_ee_eeH_HWW_ecm365', 'wzp6_ee_mumuH_HWW_ecm365'],
        'ZHZZ': ['wzp6_ee_eeH_HZZ_ecm365', 'wzp6_ee_mumuH_HZZ_ecm365'],
    },
    'backgrounds': {
        'WW': ['p8_ee_WW_ecm365'],
        'ZZ': ['p8_ee_ZZ_ecm365'],
        'Zgamma': [
            'wzp6_ee_mumu_ecm365',
            'wzp6_ee_ee_Mee_30_150_ecm365',
            'p8_ee_Zqq_ecm365',
        ],
        
        # 'ZHnonhad': [
        #     'wzp6_ee_eeH_Htautau_ecm365',
        #     'wzp6_ee_mumuH_Htautau_ecm365',
        #     'wzp6_ee_eeH_HWW_ecm365',
        #     'wzp6_ee_mumuH_HWW_ecm365',
        #     'wzp6_ee_eeH_HZZ_ecm365',
        #     'wzp6_ee_mumuH_HZZ_ecm365',
        # ],

    },
}

if showFirstGen:
    plots['ZH']['signal'].update({
        'ZHuu': ['wzp6_ee_eeH_Huu_ecm365', 'wzp6_ee_mumuH_Huu_ecm365'],
        'ZHdd': ['wzp6_ee_eeH_Hdd_ecm365', 'wzp6_ee_mumuH_Hdd_ecm365'],
    })

if showFV:
    plots['ZH']['signal'].update({
        'ZHcu': ['wzp6_ee_eeH_Hcu_ecm365', 'wzp6_ee_mumuH_Hcu_ecm365'],
        'ZHbs': ['wzp6_ee_eeH_Hbs_ecm365', 'wzp6_ee_mumuH_Hbs_ecm365'],
        'ZHbd': ['wzp6_ee_eeH_Hbd_ecm365', 'wzp6_ee_mumuH_Hbd_ecm365'],
        'ZHsd': ['wzp6_ee_eeH_Hsd_ecm365', 'wzp6_ee_mumuH_Hsd_ecm365'],
    })
    
legend = {}
for procType in plots['ZH']:
    for proc in plots['ZH'][procType]:
        legend[proc] = processLabels[proc]

# override default legend titles with e.g.
legend['Zgamma'] = 'Z/#gamma*'
