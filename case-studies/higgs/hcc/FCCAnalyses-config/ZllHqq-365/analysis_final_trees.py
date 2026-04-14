import os, sys

# import common definitions
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_final_common import *

outputDir += '/trees'

# produces ROOT TTrees, default is False
doTree = True
saveTabular = False

# Dictionary of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "finalsel": final_selec,
}

# Dictionary of the variables for the branches. Only relevant is name (name of branch).
branchList = {
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
    "jets_d23": {
        "name": "event_d23",
        "title": "d_{23}",
        "bin": 50,
        "xmin": 0,
        "xmax": 2000.0,
    },
    "jets_d34": {
        "name": "event_d34",
        "title": "d_{34}",
        "bin": 50,
        "xmin": 0,
        "xmax": 1000.0,
    },
    "jets_d45": {
        "name": "event_d45",
        "title": "d_{45}",
        "bin": 50,
        "xmin": 0,
        "xmax": 500.0,
    },
    "N_extraleptons": {
        "name": "n_extraleptons",
        "title": "N(l^{highE,extra})",
        "bin": 5,
        "xmin": -0.5,
    "xmax": 4.5,
    },
    "hadronic_mass": {
        "name": "higgs_hadronic_m",
        "title": "m_{jets} [GeV]",
        "bin": 80,
        "xmin": 50,
        "xmax": 140,
    },
    "missing_e": {
        "name": "etmiss",
        "title": "E_{miss} [GeV]",
        "bin": 60,
        "xmin": 0,
        "xmax": 30,
    },
    "zed_flavour": {
        "name": "zed_leptonic_flavour",
        "title": "Z flavour",
        "bin": 3,
        "xmin": -0.5,
        "xmax": 2.5,
    },
    "m_recoil": {
        "name": "zed_leptonic_recoil_m",
        "title": "m_{recoil} [GeV]",
        "bin": 80,
        "xmin": 120,
        "xmax": 140,
    },
   "HiggsDecay": {
       "name":"MC_HiggsDecay",
       "title":"Higgs decay",
       "bin":70,
       "xmin":0,
       "xmax":70
   }
}

# Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files.
# "name" is the name of the variable in the input file,
# "title" is the x-axis label of the histogram,
# "bin" the number of bins of the histogram,
# "xmin" the minimum x-axis value
# "xmax" the maximum x-axis value.
histoList = {}
