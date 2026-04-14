analysis = 'ZvvHqq-365'
production = 'winter2023'
detector = 'IDEA'
sqrts = 365 # GeV
lumiRef = 3.0e3 # fb-1

print("")
print('-' * 120)
print("")
print('%-35s: %s' % ('Analysis', analysis))
print('%-35s: %s' % ('Production', production))
print('%-35s: %s' % ('Detector', detector))
print('%-35s: %d' % ('Energy [GeV]', sqrts))
print('%-35s: %.1f' % ('Luminosity [ab-1]', lumiRef/1e3))

import getpass
user = getpass.getuser()

import socket
hostname = socket.gethostname()

# Directory that will contain the output files
basedir = ''
import re
if user == 'gmarchio':
    if re.match(r'^lxplus.*\.cern\.ch$', hostname):
        hostname = 'lxplus.cern.ch'
        basedir = '/eos/user/g/gmarchio/fcc/analysis/selection/%s/%s/%s/' % (analysis, production, detector)
    elif hostname == 'apcatlas01.in2p3.fr':
        basedir = '/home/gmarchio/work/fcc/analysis/fcc-hqq-analysis/selection/output/%s/%s/%s/' % (analysis, production, detector)
print('%-35s: %s' % ('Base directory for output', basedir))

# Dictionary that contains all the cross section informations etc...
procDict = 'FCCee_procDict_%s_%s.json' % (production, detector)
# print('%-35s: %s' % ('Dictionary', procDict))
# additional custom samples
procDictAdd = {
    }

# Number of CPUs to use
nCPUS = 96

# List of samples
process_list_sig = {
    # Z(nunu)H
    'wzp6_ee_nunuH_Hbb_ecm365' : {},
    'wzp6_ee_nunuH_Hcc_ecm365' : {},
    'wzp6_ee_nunuH_Hss_ecm365' : {},
    'wzp6_ee_nunuH_Hgg_ecm365' : {},
    'wzp6_ee_nunuH_Htautau_ecm365' : {},
    'wzp6_ee_nunuH_HWW_ecm365' : {},
    'wzp6_ee_nunuH_HZZ_ecm365' : {},
#    'wzp6_ee_nunuH_Huu_ecm365' : {},
#    'wzp6_ee_nunuH_Hdd_ecm365' : {},
#    'wzp6_ee_nunuH_Hbs_ecm365' : {},
#    'wzp6_ee_nunuH_Hbd_ecm365' : {},
#    'wzp6_ee_nunuH_Hsd_ecm365' : {},
#    'wzp6_ee_nunuH_Hcu_ecm365' : {},
    # Z(bb)H
    'wzp6_ee_bbH_Hbb_ecm365' : {},
    'wzp6_ee_bbH_Hcc_ecm365' : {},
    'wzp6_ee_bbH_Hss_ecm365' : {},
    'wzp6_ee_bbH_Hgg_ecm365' : {},
    'wzp6_ee_bbH_Htautau_ecm365' : {},
    'wzp6_ee_bbH_HWW_ecm365' : {},
    'wzp6_ee_bbH_HZZ_ecm365' : {},
    # Z(cc)H
    'wzp6_ee_ccH_Hbb_ecm365' : {},
    'wzp6_ee_ccH_Hcc_ecm365' : {},
    'wzp6_ee_ccH_Hss_ecm365' : {},
    'wzp6_ee_ccH_Hgg_ecm365' : {},
    'wzp6_ee_ccH_Htautau_ecm365' : {},
    'wzp6_ee_ccH_HWW_ecm365' : {},
    'wzp6_ee_ccH_HZZ_ecm365' : {},
    # Z(ss)H
    'wzp6_ee_ssH_Hbb_ecm365' : {},
    'wzp6_ee_ssH_Hcc_ecm365' : {},
    'wzp6_ee_ssH_Hss_ecm365' : {},
    'wzp6_ee_ssH_Hgg_ecm365' : {},
    'wzp6_ee_ssH_Htautau_ecm365' : {},
    'wzp6_ee_ssH_HWW_ecm365' : {},
    'wzp6_ee_ssH_HZZ_ecm365' : {},
    # Z(qq)H
    'wzp6_ee_qqH_Hbb_ecm365' : {},
    'wzp6_ee_qqH_Hcc_ecm365' : {},
    'wzp6_ee_qqH_Hss_ecm365' : {},
    'wzp6_ee_qqH_Hgg_ecm365' : {},
    'wzp6_ee_qqH_Htautau_ecm365' : {},
    'wzp6_ee_qqH_HWW_ecm365' : {},
    'wzp6_ee_qqH_HZZ_ecm365' : {},
}
process_list_bkg = {
    'p8_ee_ZZ_ecm365': {},
    'p8_ee_WW_ecm365': {},
    'p8_ee_Zqq_ecm365': {},
    'wzp6_ee_nuenueZ_ecm365' : {},
    'p8_ee_tt_ecm365': {},
}
processList = process_list_sig | process_list_bkg
# for debug use only one sample
# processList = { 'wzp6_ee_nunuH_Hbb_ecm365' : {} }

# dictionary of possible cuts
cutDict = {
    'selNone' : {
        'cut' : '(0<1)',
        'label' : 'No cuts',
    },
    'sel_nolep' : {
        'cut': 'isolated_leptons_pmax<1',
        'label' : 'No iso-leptons with p>1 GeV',
    },
    'sel_jetE' : {
        'cut' : '(jet1_E>40 && jet1_E<180 && jet2_E>15 && jet2_E<100)',
        'label' : '15<E_j1<105, 10<E_j2<70 GeV',
    },
    'sel_cosThetaJJ' : {
        'cut' : 'higgs_hadronic_cos_theta<0.9',
        'label' : '|cos(theta_jj)|<0.9',
    },
    'sel_cosSumThetaJJ' : {
        'cut' : 'higgs_hadronic_cos_dTheta_jj>0.5',
        'label' : 'cos(th_j1+th_j2)>0.5',
    },
    'sel_cosDPhiJJ' : {
        'cut' : 'higgs_hadronic_cos_dPhi_jj<0.999',
        'label' : 'cos(phi_j1-phi_j2)<0.999',
    },
    'sel_mvis_mmiss'   : {
        'cut' : '(mvis > 80 && mvis < 280 && higgs_hadronic_recoil_m>50 && higgs_hadronic_recoil_m<350)',
        'label' : '80<mvis<280, 50<mmiss<350 GeV'
    },    
    'sel_dmergeok'   : {
        # '(event_d23 >0.) && (event_d34>0.) && (event_d45>0.)'
        'cut' : '(event_d23 >0.) && (event_d34>0.)',
        'label' : 'd23>0, d34>0',
    },
    'sel_Hhad' : {
        'cut' : '(MC_HiggsDecay<=10 || MC_HiggsDecay==40 || MC_HiggsDecay==51)',
        'label' : 'Hadronic Higgs decays',
    },
    'sel_Hnonhad' : {
        'cut' : '(MC_HiggsDecay>10 && MC_HiggsDecay!=40 && MC_HiggsDecay!=51)',
        'label' : 'Non-hadronic Higgs decays',
    },
}

# the selection to be applied:
sel = [
    'selNone',
    'sel_nolep',
    'sel_jetE',
    'sel_cosThetaJJ',
    'sel_cosSumThetaJJ',
    'sel_cosDPhiJJ',
    'sel_mvis_mmiss',
    'sel_dmergeok',
]
final_sel_cut = 'sel_dmergeok'

# the cuts for each selection step
cuts = {}
print('Cuts:')
for i, cut in enumerate(sel):
    if i==0:
        cuts[cut] = cutDict[cut]['cut']
    else:
        cuts[cut] = cuts[sel[i-1]] + ' && ' + cutDict[cut]['cut']
    print('  %s : %s' % (cut, cuts[cut]))

# the final selection
final_selec = cuts[final_sel_cut]

# Dictionary of the list of cuts when applying the selection and saving the trees.
# The key is the name of the selection that will be added to the output file
cutList_treeOnly = {
    'trainNN' : final_selec,
}

# Dictionary of the list of cuts for hists only.
# The key is the name of the selection that will be added to the output file.
cutList_histOnly = cuts
cutList_histOnly['finalsel'    ] = final_selec
cutList_histOnly['finalsel_hhad'    ] = final_selec + ' && ' + cutDict['sel_Hhad']['cut']
cutList_histOnly['finalsel_hnonhad' ] = final_selec + ' && ' + cutDict['sel_Hnonhad']['cut']

# Dictionary of colors
# 18 colors generated with https://mokole.com/palette.html
colordict = {
    'darkslategray':  '#2f4f4f',
    'maroon': '#800000',
    'green':  '#008000',
    'purple': '#800080',
    'red':  '#ff0000',
    'darkorange': '#ff8c00',
    'yellow':  '#ffff00',
    'mediumblue': '#0000cd',
    'lawngreen':  '#7cfc00',
    'turquoise': '#40e0d0',
    'mediumspringgreen':  '#00fa9a',
    'royalblue': '#4169e1',
    'darksalmon':  '#e9967a',
    'deepskyblue': '#00bfff',
    'fuchsia':  '#ff00ff',
    'khaki': '#f0e68c',
    'plum':  '#dda0dd',
    'deeppink': '#ff1493',
    # add black
    'black': '#000000'
}

processColors = {
    'ZHbb' : 'darkslategray',
    'ZHcc' : 'maroon',
    'ZHss' : 'green',
    'ZHgg' : 'purple',
    'ZHother' : 'red',
    'ZHtautau' : 'red',
    'ZHWW' : 'darkorange',
    'ZHZZ' : 'yellow',
    'ZHuu' : 'mediumblue',
    'ZHdd' : 'lawngreen',
    'ZHbs' : 'turquoise',
    'ZHbd' : 'mediumspringgreen',
    'ZHsd' : 'royalblue',
    'ZHcu' : 'darksalmon',
    'qqH' : 'deepskyblue',
    'ZZ': 'fuchsia',
    'WW': 'khaki',
    'Zqq': 'plum',
    'nuenueZ' : 'deeppink',
    'ttbar' : 'black'
    }

processColors.update({
    'wzp6_ee_nunuH_Hbb_ecm365' : processColors['ZHbb'],
    'wzp6_ee_nunuH_Hcc_ecm365' : processColors['ZHcc'],
    'wzp6_ee_nunuH_Hss_ecm365' : processColors['ZHss'],
    'wzp6_ee_nunuH_Hgg_ecm365' : processColors['ZHgg'],
    'wzp6_ee_nunuH_Htautau_ecm365' : processColors['ZHtautau'],
    'wzp6_ee_nunuH_HWW_ecm365' : processColors['ZHWW'],
    'wzp6_ee_nunuH_HZZ_ecm365' : processColors['ZHZZ'],
    'wzp6_ee_nunuH_Huu_ecm365' : processColors['ZHuu'],
    'wzp6_ee_nunuH_Hdd_ecm365' : processColors['ZHdd'],
    'wzp6_ee_nunuH_Hbs_ecm365' : processColors['ZHbs'],
    'wzp6_ee_nunuH_Hbd_ecm365' : processColors['ZHbd'],
    'wzp6_ee_nunuH_Hsd_ecm365' : processColors['ZHsd'],
    'wzp6_ee_nunuH_Hcu_ecm365' : processColors['ZHcu'],
    'p8_ee_ZZ_ecm365': processColors['ZZ'],
    'p8_ee_WW_ecm365': processColors['WW'],
    'p8_ee_Zqq_ecm365': processColors['Zqq'],
    'p8_ee_tt_ecm365': processColors['ttbar'],
    'wzp6_ee_nuenueZ_ecm365' : processColors['nuenueZ'],
})

processLabels = {
    'wzp6_ee_nunuH_Hbb_ecm365' : '#nu#bar{#nu}H(b#bar{b})',
    'wzp6_ee_nunuH_Hcc_ecm365' : '#nu#bar{#nu}H(c#bar{c})',
    'wzp6_ee_nunuH_Hss_ecm365' : '#nu#bar{#nu}H(s#bar{s})',
    'wzp6_ee_nunuH_Huu_ecm365' : '#nu#bar{#nu}H(d#bar{d})',
    'wzp6_ee_nunuH_Hdd_ecm365' : '#nu#bar{#nu}H(u#bar{u})',
    'wzp6_ee_nunuH_Hgg_ecm365' : '#nu#bar{#nu}H(gg)',
    'wzp6_ee_nunuH_Htautau_ecm365' : '#nu#bar{#nu}H(#tau#tau)',
    'wzp6_ee_nunuH_HWW_ecm365' : '#nu#bar{#nu}H(WW)',
    'wzp6_ee_nunuH_HZZ_ecm365' : '#nu#bar{#nu}H(ZZ)',
    'wzp6_ee_nunuH_Hnonhad_ecm365' : '#nu#bar{#nu}H(other)',
    'p8_ee_ZZ_ecm365' : 'ZZ',
    'p8_ee_WW_ecm365' : 'WW',
    'p8_ee_Zqq_ecm365' : 'Z/#gamma*(q#bar{q})',
    'wzp6_ee_nuenueZ_ecm365' : '#nu_{e}#bar{#nu}_{e}Z',
    'p8_ee_tt_ecm365': 't#bar{t}',
}

processLabels.update({
    'ZHbb' : '#nu#bar{#nu}H(b#bar{b})',
    'ZHcc' : '#nu#bar{#nu}H(c#bar{c})',
    'ZHss' : '#nu#bar{#nu}H(s#bar{s})',
    'ZHuu' : '#nu#bar{#nu}H(d#bar{d})',
    'ZHdd' : '#nu#bar{#nu}H(u#bar{u})',
    'ZHgg' : '#nu#bar{#nu}H(gg)',
    'ZHtautau' : '#nu#bar{#nu}H(#tau#tau)',
    'ZHWW' : '#nu#bar{#nu}H(WW)',
    'ZHZZ' : '#nu#bar{#nu}H(ZZ)',
    'ZHother' : '#nu#bar{#nu}H(other)',
    'ZHcu' : '#nu#bar{#nu}H(c#bar{u})',
    'ZHbs' : '#nu#bar{#nu}H(b#bar{s})',
    'ZHbd' : '#nu#bar{#nu}H(b#bar{d})',
    'ZHsd' : '#nu#bar{#nu}H(s#bar{d})',
    'ZZ' : 'ZZ',
    'WW' : 'WW',
    'Zqq' : 'Z/#gamma*(q#bar{q})',
    'nuenueZ' : '#nu_{e}#bar{#nu}_{e}Z',
    'qqH' : 'q#bar{q}H',
    'ttbar' : 't#bar{t}',
})


#
# load the dictionary of processes
#
dictFound=False
import os
procDictFile = ""
if os.path.isfile('./' + procDict):
    procDictFile = './' + procDict
    dictFound=True
else:
    #print('Dictionary not found in local directory, trying alternative folders: ')
    procFolders = os.getenv('FCCDICTSDIR').split(':')
    if len(procFolders) == 0:
        folder = '/cvmfs/fcc.cern.ch/FCCDicts'
        #print(folder)
        if os.path.isfile(folder + '/' + procDict):
            procDictFile = folder + '/' + procDict
            dictFound = True
    else:
        for folder in procFolders:
            #print(folder)
            if os.path.isfile(folder + '/' + procDict):
                procDictFile = folder + '/' + procDict
                dictFound = True
                break
if not dictFound:
    print('Dictionary not found, exiting')
    exit(1)

print('\n%-35s: %s' % ('Dictionary', procDictFile))

f = open(procDictFile, 'r')
import json
procDictionary = json.load(f)

# expand procDict with additional samples
# print('Adding to dictionary the private samples (if any)')
procDictionary.update(procDictAdd)
print('%-35s: ' % ('Extra samples added to dictionary'), end="")
for sample in procDictAdd: print(sample, end=" ")
print("\n")
print('-' * 120)
print("\n")
