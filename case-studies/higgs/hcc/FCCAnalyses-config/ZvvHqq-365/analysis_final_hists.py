import os, sys

# import common definitions
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_final_common import *

outputDir += '/hists'

# produces ROOT TTrees, default is False
doTree = False

# save cutflow, normalised to luminosity intLumi
# histograms will be scaled to 1/pb instead
saveTabular = True
doScale = True  # scale to reference lumi
intLumi = lumiRef*1e3  # reference lumi in 1/pb

cutList = cutList_histOnly

# Dictionary for the ouput variable/hitograms.
# The key is the name of the variable in the output files.
# "name" is the name of the variable in the input file
# "title" is the x-axis label of the histogram
# "bin" the number of bins of the histogram
# "xmin" the minimum x-axis value
# "xmax" the maximum x-axis value.
histoList = {
    'jet1_E':{'name':'jet1_E','title':'Jet1 E [GeV]','bin':70,'xmin':0,'xmax':140},
    'jet2_E':{'name':'jet2_E','title':'Jet2 E [GeV]','bin':70,'xmin':0,'xmax':140},  
    'missing_e':{'name':'pmiss','title':'p_{miss} [GeV]','bin':60,'xmin':0,'xmax':120},
    'higgs_hadronic_mass':{'name':'higgs_hadronic_m','title':'Dijet invariant mass [GeV]','bin':100,'xmin':80,'xmax':280},
    'mvis':{'name':'mvis','title':'Visible mass [GeV]','bin':100,'xmin':80,'xmax':280},
    'mmiss':{'name':'higgs_hadronic_recoil_m','title':'m_{miss} [GeV]','bin':150,'xmin':50,'xmax':350},
    'mvis_zoom':{'name':'mvis','title':'Visible mass [GeV]','bin':80,'xmin':70,'xmax':150},
    'higgs_hadronic_recoil_mass_zoom':{'name':'higgs_hadronic_recoil_m','title':'m_{miss} [GeV]','bin':100,'xmin':50,'xmax':350},
    'jet1_nconst':{'name':'jet1_nconst','title':'Nparts in Jets 1','bin':60,'xmin':0,'xmax':60},
    'jet2_nconst':{'name':'jet2_nconst','title':'Nparts in Jets 2','bin':60,'xmin':0,'xmax':60},
    'higgs_hadronic_cos_theta':{'name':'higgs_hadronic_cos_theta','title':'|cos({theta}_{jj})|','bin':50,'xmin':0,'xmax':1},
    'higgs_hadronic_cosSumThetaJJ':{'name':'higgs_hadronic_cos_dTheta_jj','title':'|cos(#theta_{j1}+#theta_{j2})|','bin':50,'xmin':0,'xmax':1},
    'higgs_hadronic_cosDeltaPhiJJ':{'name':'higgs_hadronic_cos_dPhi_jj','title':'cos(#phi_{j1}-#phi_{j2})','bin':50,'xmin':0,'xmax':1},
    'higgs_hadronic_cosDeltaPhiJJ_zoom':{'name':'higgs_hadronic_cos_dPhi_jj','title':'cos(#phi_{j1}-#phi_{j2})','bin':100,'xmin':0.95,'xmax':1},
    'jets_d23':{'name':'event_d23','title':'d_{23}','bin':50,'xmin':0,'xmax':2500},
    'jets_d34':{'name':'event_d34','title':'d_{34} jet distance','bin':50,'xmin':0,'xmax':1000},
    'jets_d45':{'name':'event_d45','title':'d_{45}','bin':50,'xmin':0,'xmax':500},
    'n_all_leptons':{'name':'n_all_leptons','title':'N(leptons)','bin':3,'xmin':0,'xmax':3},
    'n_selected_leptons':{'name':'n_selected_leptons','title':'N(high-p leptons)','bin':3,'xmin':0,'xmax':3},
    'leptons_p':{'name':'leptons_p','title':'p(leptons)','bin':100,'xmin':0,'xmax':100},
    'pmiss':{'name':'pmiss','title':'p_{miss} [GeV]','bin':50,'xmin':20,'xmax':70},
    # 'higgs_hadronic_mass':{'name':'higgs_hadronic_m','title':'m_{jj} [GeV]','bin':80,'xmin':100,'xmax':135},
    # 'missing_e' : {'name':'pmiss','title':'p_{miss} [GeV]','bin':80,'xmin':20,'xmax':100},
    # 'mvis'      : {'name':'mvis','title':'m_{vis} [GeV]','bin':80,'xmin':70,'xmax':150},
    # 'mmiss'     : {'name':'higgs_hadronic_recoil_m','title':'m_{miss} [GeV]','bin':150,'xmin':20,'xmax':170},
    'HiggsDecay': {'name':'MC_HiggsDecay','title':'Higgs decay', 'bin':70,'xmin':0,'xmax':70},
    "jet1_isB": {
        "name": "jet1_isB",
        "title": "isB(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isC": {
        "name": "jet1_isC",
        "title": "isC(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isG": {
        "name": "jet1_isG",
        "title": "isG(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isS": {
        "name": "jet1_isS",
        "title": "isS(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isU": {
        "name": "jet1_isU",
        "title": "isU(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isD": {
        "name": "jet1_isD",
        "title": "isD(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet1_isTAU": {
        "name": "jet1_isTAU",
        "title": "isTAU(j1)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isB": {
        "name": "jet2_isB",
        "title": "isB(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isC": {
        "name": "jet2_isC",
        "title": "isC(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isG": {
        "name": "jet2_isG",
        "title": "isG(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isS": {
        "name": "jet2_isS",
        "title": "isS(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isU": {
        "name": "jet2_isU",
        "title": "isU(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isD": {
        "name": "jet2_isD",
        "title": "isD(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
    "jet2_isTAU": {
        "name": "jet2_isTAU",
        "title": "isTAU(j2)",
        "bin": 100,
        "xmin": 0.0,
        "xmax": 1.0,
    },
}
