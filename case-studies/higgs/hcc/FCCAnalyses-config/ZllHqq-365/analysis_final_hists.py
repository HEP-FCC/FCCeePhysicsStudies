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
    "zed_flavour": {
        "name": "zed_leptonic_flavour",
        "title": "Z flavour",
        "bin": 3,
        "xmin": -0.5,
        "xmax": 2.5,
    },
    "all_leptons_p": {
        "name": "leptons_p",
        "title": "p(l^{rec}) [GeV]",
        "bin": 48,
        "xmin": 0,
        "xmax": 120,
    },
    "zed_leptons_p": {
        "name": "zed_leptons_p",
        "title": "p(l^{sel}) [GeV]",
        "bin": 70,
        "xmin": 0,
        "xmax": 140,
    },
    "extraleptons_p": {
        "name": "extraleptons_p",
        "title": "p(l^{iso,extra}) [GeV]",
        "bin": 70,
        "xmin": 0,
        "xmax": 140,
    },
    "N_extra_leptons": {
        "name": "n_extraleptons",
        "title": "N(l^{extra})",
        "bin": 5,
        "xmin": -0.5,
        "xmax": 4.5,
    },
    "all_jets_p": {
        "name": "jet_p",
        "title": "E^{j} [GeV]",
        "bin": 70,
        "xmin": 0,
        "xmax": 140,
    },
    "jets_p": {
        "name": "selected_jets_p",
        "title": "p^{j} [GeV]",
        "bin": 70,
        "xmin": 0,
        "xmax": 140,
    },
    "N_jets": {
        "name": "n_selected_jets",
        "title": "N_{jets}",
        "bin": 10,
        "xmin": -0.5,
        "xmax": 9.5,
    },
    "cos_theta_Z": {
        "name": "zed_leptonic_cos_theta",
        "title": "|cos#theta_{ll}|",
        "bin": 20,
        "xmin": 0,
        "xmax": 1,
    },
    "missing_e": {
        "name": "etmiss",
        "title": "E_{miss} [GeV]",
        "bin": 60,
        "xmin": 0,
        "xmax": 60,
    },
    "dilepton_mass": {
        "name": "zed_leptonic_m",
        "title": "m_{ll} [GeV]",
        "bin": 110,
        "xmin": 0,
        "xmax": 220,
    },
    "dilepton_mass_2": {
        "name": "zed_leptonic_m",
        "title": "m_{ll} [GeV]",
        "bin": 80,
        "xmin": 70,
        "xmax": 110,
    },
    "dilepton_charge": {
        "name": "zed_leptonic_charge",
        "title": "q_{ll}",
        "bin": 5,
        "xmin": -2.5,
        "xmax": 2.5,
    },
    "hadronic_mass": {
        "name": "higgs_hadronic_m",
        "title": "m_{jets} [GeV]",
        "bin": 110,
        "xmin": 0,
        "xmax": 220,
    },
    "hadronic_mass_2": {
        "name": "higgs_hadronic_m_2",
        "title": "m_{jets} [GeV]",
        "bin": 110,
        "xmin": 0,
        "xmax": 220,
    },
    "hadronic_mass_zoom": {
        "name": "higgs_hadronic_m",
        "title": "m_{jets} [GeV]",
        "bin": 100,
        "xmin": 50,
        "xmax": 150,
    },
    "m_recoil": {
        "name": "zed_leptonic_recoil_m",
        "title": "m_{recoil} [GeV]",
        "bin": 160,
        "xmin": 120,
        "xmax": 200,
    },
    "m_recoil_2": {
        "name": "zed_leptonic_recoil_m",
        "title": "m_{recoil} [GeV]",
        "bin": 160,
        "xmin": 70,
        "xmax": 210,
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
    "jet2_E": {
        "name": "jet2_E",
        "title": "E(j_{2}) [GeV]",
        "bin": 100,
        "xmin": 0,
        "xmax": 200,
    },
}
