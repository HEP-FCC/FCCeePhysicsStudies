analysis = 'ZllHqq-365'
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
#    "wzp6_ee_eeH_Huu_ecm365": {
#        "numberOfEvents": 400000,
#        "sumOfWeights": 400000.0,
#        "crossSection": 6.4472186e-10,
#        "kfactor": 1.0,
#        "matchingEfficiency": 1.0
#    },
# }


# Number of CPUs to use
nCPUS = 96

# List of samples
process_list_sig = {
    'wzp6_ee_eeH_Hbb_ecm365': {},
    'wzp6_ee_eeH_Hcc_ecm365': {},
    'wzp6_ee_eeH_Hgg_ecm365': {},
    'wzp6_ee_eeH_Hss_ecm365': {},
    'wzp6_ee_eeH_Htautau_ecm365': {},
    'wzp6_ee_eeH_HWW_ecm365': {},
    'wzp6_ee_eeH_HZZ_ecm365': {},
#    'wzp6_ee_eeH_Huu_ecm365': {},
#    'wzp6_ee_eeH_Hdd_ecm365': {},
#    'wzp6_ee_eeH_Hbs_ecm365': {},
#    'wzp6_ee_eeH_Hbd_ecm365': {},
#    'wzp6_ee_eeH_Hsd_ecm365': {},
#    'wzp6_ee_eeH_Hcu_ecm365': {},
    #
    'wzp6_ee_mumuH_Hbb_ecm365': {},
    'wzp6_ee_mumuH_Hcc_ecm365': {},
    'wzp6_ee_mumuH_Hgg_ecm365': {},
    'wzp6_ee_mumuH_Hss_ecm365': {},
    'wzp6_ee_mumuH_Htautau_ecm365': {},
    'wzp6_ee_mumuH_HWW_ecm365': {},
    'wzp6_ee_mumuH_HZZ_ecm365': {},
#    'wzp6_ee_mumuH_Huu_ecm365': {},
#    'wzp6_ee_mumuH_Hdd_ecm365': {},
#    'wzp6_ee_mumuH_Hbs_ecm365': {},
#    'wzp6_ee_mumuH_Hbd_ecm365': {},
#    'wzp6_ee_mumuH_Hsd_ecm365': {},
#    'wzp6_ee_mumuH_Hcu_ecm365': {},
}
process_list_bkg = {
    'p8_ee_ZZ_ecm365': {},
    'p8_ee_WW_ecm365': {},
    'p8_ee_Zqq_ecm365': {},
    'wzp6_ee_mumu_ecm365': {},
    'wzp6_ee_ee_Mee_30_150_ecm365': {},
    'p8_ee_tt_ecm365': {},
}
processList = process_list_sig | process_list_bkg

# dictionary of possible cuts
cutDict = {
    'selNone' : {
        'cut' : '(0<1)',
        'label' : 'No cuts',
    },
    'sel_lep' : {
        'cut' : 'isolated_leptons_pmax>40',
        'label' : '>0 iso-leptons with p>40 GeV',
    },
    'sel_Z' : {
        'cut' : '(zed_leptonic_flavour>0)',
        'label' : 'one Z->ll candidate',
        },
    'sel_mZ' : {
        'cut' : '(zed_leptonic_m > 81 && zed_leptonic_m < 101)',
        'label' : 'm(ll) 81-101 GeV',
        },
    'sel_cosThetaZ' : {
        'cut' : '(zed_leptonic_cos_theta < 0.8)',
        'label' : '|cos(theta_ll)|<0.8',
    },
    'sel_mrecoil' : {
        'cut' : '(zed_leptonic_recoil_m > 120 && zed_leptonic_recoil_m < 200)',
        'label' : 'm(recoil) 120-200 GeV',
    },
    'sel_ej2' : {
        'cut' : 'jet2_E>15',
        'label' : 'E(j2)>15 GeV',
    },
    'sel_mjj' : {
      #  'cut' : '(higgs_hadronic_m>100 && higgs_hadronic_m<140)',
      #  'label' : '100<m(jets)<140 GeV',
        'cut' : '(higgs_hadronic_m>50 && higgs_hadronic_m<140)',
        'label' : '50<m(jets)<140 GeV',
    },
    'sel_emiss' : {
        'cut' : '(etmiss < 30)',
        'label' : 'Emiss < 30 GeV',
    },                
    'sel_leptonveto' : {
        'cut' : '(n_iso_leptons<3)',
        #'label' : 'max p(extra lep) < 25 GeV',
        'label' : '<=2 iso leptons',
    },
    'sel_dmergeok'   : {
        # '(event_d23 >0.) && (event_d34>0.) && (event_d45>0.)'
        'cut' : '(event_d23 >0.) && (event_d34>0.)',
        'label' : 'd23>0, d34>0',
    },
    'sel_Zee' : {
        'cut' : '(zed_leptonic_flavour==1)',
        'label' : 'l=e',
    },
    'sel_Zmumu' : {
        'cut' : '(zed_leptonic_flavour==2)',
        'label' : 'l=mu',
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
    'sel_lep',
    'sel_Z',
    'sel_mZ',
    'sel_cosThetaZ',
    'sel_mrecoil',
    'sel_ej2',
    # 'sel_mjj',     # removed, will kill H(tautau) otherwise)
    # 'sel_emiss',   # removed, will kill H(tautau) otherwise)
    'sel_leptonveto',
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
cutList_histOnly['finalsel_e'  ] = final_selec + ' && ' + cutDict['sel_Zee']['cut']
cutList_histOnly['finalsel_mu' ] = final_selec + ' && ' + cutDict['sel_Zmumu']['cut']
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
#    'ZHuu' : 'mediumblue',
#    'ZHdd' : 'lawngreen',
#    'ZHbs' : 'turquoise',
#    'ZHbd' : 'mediumspringgreen',
#    'ZHsd' : 'royalblue',
#    'ZHcu' : 'darksalmon',
    'ZZ': 'fuchsia',
    'WW': 'khaki',
    'Zgamma': 'plum',
    'Zll' : 'deeppink',
    'Zqq' : 'deepskyblue',
    'ttbar' : 'darksalmon' 
    }

processColors.update({
    'wzp6_ee_eeH_Hbb_ecm365' : processColors['ZHbb'],
    'wzp6_ee_eeH_Hcc_ecm365' : processColors['ZHcc'],
    'wzp6_ee_eeH_Hss_ecm365' : processColors['ZHss'],
    'wzp6_ee_eeH_Hgg_ecm365' : processColors['ZHgg'],
    'wzp6_ee_eeH_Htautau_ecm365' : processColors['ZHtautau'],
    'wzp6_ee_eeH_HWW_ecm365' : processColors['ZHWW'],
    'wzp6_ee_eeH_HZZ_ecm365' : processColors['ZHZZ'],
#    'wzp6_ee_eeH_Huu_ecm365' : processColors['ZHuu'],
#    'wzp6_ee_eeH_Hdd_ecm365' : processColors['ZHdd'],
#    'wzp6_ee_eeH_Hbs_ecm365' : processColors['ZHbs'],
#    'wzp6_ee_eeH_Hbd_ecm365' : processColors['ZHbd'],
#    'wzp6_ee_eeH_Hsd_ecm365' : processColors['ZHsd'],
#    'wzp6_ee_eeH_Hcu_ecm365' : processColors['ZHcu'],
    'p8_ee_ZZ_ecm365': processColors['ZZ'],
    'p8_ee_WW_ecm365': processColors['WW'],
    'p8_ee_Zqq_ecm365': processColors['Zqq'],
    'wzp6_ee_mumu_ecm365': processColors['Zll'],
    'wzp6_ee_ee_Mee_30_150_ecm365': processColors['Zll'],
    'p8_ee_tt_ecm365': processColors['ttbar'],
})

processLabels = {
    'wzp6_ee_eeH_Hbb_ecm365' : 'eeH(b#bar{b})',
    'wzp6_ee_eeH_Hcc_ecm365' : 'eeH(c#bar{c})',
    'wzp6_ee_eeH_Hss_ecm365' : 'eeH(s#bar{s})',
#    'wzp6_ee_eeH_Huu_ecm365' : 'eeH(d#bar{d})',
#    'wzp6_ee_eeH_Hdd_ecm365' : 'eeH(u#bar{u})',
    'wzp6_ee_eeH_Hgg_ecm365' : 'eeH(gg)',
    'wzp6_ee_eeH_Htautau_ecm365' : 'eeH(#tau#tau)',
    'wzp6_ee_eeH_HWW_ecm365' : 'eeH(WW)',
    'wzp6_ee_eeH_HZZ_ecm365' : 'eeH(ZZ)',
    'wzp6_ee_eeH_Hnonhad_ecm365' : 'eeH(other)',
    'wzp6_ee_mumuH_Hbb_ecm365' : '#mu#muH(b#bar{b})',
    'wzp6_ee_mumuH_Hcc_ecm365' : '#mu#muH(c#bar{c})',
    'wzp6_ee_mumuH_Hss_ecm365' : '#mu#muH(s#bar{s})',
#    'wzp6_ee_mumuH_Huu_ecm365' : '#mu#muH(d#bar{d})',
#    'wzp6_ee_mumuH_Hdd_ecm365' : '#mu#muH(u#bar{u})',
    'wzp6_ee_mumuH_Hgg_ecm365' : '#mu#muH(gg)',
    'wzp6_ee_mumuH_Htautau_ecm365' : '#mu#muH(#tau#tau)',
    'wzp6_ee_mumuH_HWW_ecm365' : '#mu#muH(WW)',
    'wzp6_ee_mumuH_HZZ_ecm365' : '#mu#muH(ZZ)',
    'wzp6_ee_mumuH_Hnonhad_ecm365' : '#mu#muH(other)',
    'p8_ee_ZZ_ecm365' : 'ZZ',
    'p8_ee_WW_ecm365' : 'WW',
    'p8_ee_Zqq_ecm365' : 'Z/#gamma*(q#bar{q})',
    'wzp6_ee_mumu_ecm365': 'Z/#gamma*(#mu#mu)',
    'wzp6_ee_ee_Mee_30_150_ecm365': 'Z/#gamma*(ee)',
    'p8_ee_tt_ecm365': 't#bar{t}',
}

processLabels.update({
    'ZHbb' : 'llH(b#bar{b})',
    'ZHcc' : 'llH(c#bar{c})',
    'ZHss' : 'llH(s#bar{s})',
#    'ZHuu' : 'llH(d#bar{d})',
#    'ZHdd' : 'llH(u#bar{u})',
    'ZHgg' : 'llH(gg)',
    'ZHtautau' : 'llH(#tau#tau)',
    'ZHWW' : 'llH(WW)',
    'ZHZZ' : 'llH(ZZ)',
    'ZHother' : 'llH(other)',
#    'ZHcu' : 'llH(c#bar{u})',
#    'ZHbs' : 'llH(b#bar{s})',
#    'ZHbd' : 'llH(b#bar{d})',
#    'ZHsd' : 'llH(s#bar{d})',
    'ZZ' : 'ZZ',
    'WW' : 'WW',
    'Zll' : 'Z/#gamma*(ee/#mu#mu})',
    'Zqq' : 'Z/#gamma*(q/#bar{q})',
    'Zgamma' : 'Z/#gamma*(ee/#mu#mu/q#bar{q})',
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
            print(folder)
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
