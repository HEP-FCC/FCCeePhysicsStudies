# import common definitions
import os, sys
configdir = os.getenv('FCCANACONFS')
sys.path.append(configdir)
from analysis_config import *

# Mandatory: Production tag when running over EDM4Hep centrally produced events,
# this points to the yaml files for getting sample statistics
prodTag = 'FCCee/%s/%s/' % (production, detector)

includePaths = ["functions.h"]

outputDirEos = '/eos/user/g/gmarchio/fcc-test/ZllHqq-365/analysis/root/IDEA/'
eosType = 'eosuser'

# Optional: ncpus, default is 4
# nCPUS = 32

# Optional running on HTCondor, default is False
runBatch = False
# runBatch = True

# Optional batch queue name when running on HTCondor, default is workday
# batchQueue = 'longlunch'

# Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
# compGroup = 'group_u_FCC.local_gen'


import ROOT

# ROOT.gErrorIgnoreLevel = ROOT.kFatal

import os, sys
import urllib.request


# ____________________________________________________________
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


# ____________________________________________________________


# tagger model
# model_name = 'fccee_flavtagging_edm4hep_wc_v1'
# model_dir = '/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022'
# latest particle transformer model, trainied on 9M jets in winter2023 samples, with 7 outputs
model_name = 'fccee_flavtagging_edm4hep_wc'
model_dir = '/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/'

# model files needed for unit testing in CI
url_model_dir = 'https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/'
url_model_name = 'fccee_flavtagging_edm4hep_wc_v1'
url_preproc = '{}/{}.json'.format(url_model_dir, url_model_name)
url_model = '{}/{}.onnx'.format(url_model_dir, url_model_name)

local_preproc = '{}/{}.json'.format(model_dir, model_name)
local_model = '{}/{}.onnx'.format(model_dir, model_name)

# get local file, else download from url
weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import ExclusiveJetClusteringHelper

jetFlavourHelper = None
jetClusteringHelper = None

jet_p_min = '15'
jet_p_max = '1000'
lep_p_min = '13'
lep_p_max = '160'

# jet_p_min = '15'
# jet_p_max = '100'
# lep_p_min = '25'
# lep_p_max = '80'


# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:
    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process.
    # Note: make sure you return the last dataframe
    def analysers(df):
        global jetClusteringHelper
        global jetFlavourHelper

        # SELECT LEPTONS

        df2 = (
            df
            # MC truth info
            .Alias('DaughtersIdx', 'Particle#1.index')
            .Define(
                'MC_HiggsDecay',
                'FCCAnalyses::MCParticle::get_Higgs_decay()(Particle,DaughtersIdx)',
            )
            # define an alias for muon index collection
            .Alias('Muon0', 'Muon#0.index')
            # define the muon collection
            .Define(
                'muons', 'ReconstructedParticle::get(Muon0, ReconstructedParticles)'
            )
            .Define('n_all_muons', 'ReconstructedParticle::get_n(muons)')
            # define an alias for electron index collection
            .Alias('Electron0', 'Electron#0.index')
            # define the electron collection
            .Define(
                'electrons',
                'ReconstructedParticle::get(Electron0, ReconstructedParticles)',
            )
            .Define('n_all_electrons', 'ReconstructedParticle::get_n(electrons)')
            # merge electrons and muons
            .Define('leptons', 'ReconstructedParticle::merge(electrons, muons)')
            # create branch with all lepton momenta
            .Define('leptons_p', 'ReconstructedParticle::get_p(leptons)')
            # calculate lepton isolation
            .Define("leptons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(leptons, ReconstructedParticles)")
            .Define("isolated_leptons", "FCCAnalyses::ZHfunctions::sel_iso(1.0)(leptons, leptons_iso)")
            .Define('n_all_leptons', 'ReconstructedParticle::get_n(leptons)')
            .Define('n_iso_leptons', 'ReconstructedParticle::get_n(isolated_leptons)')
            .Define('isolated_leptons_p', 'ReconstructedParticle::get_p(isolated_leptons)')
            .Define('isolated_leptons_pmax', 'Utils::getmax(isolated_leptons_p)*(n_iso_leptons>0)')
            # select muons based on p
            .Define(
                'selected_muons',
                'ReconstructedParticle::sel_p('
                + lep_p_min
                + ','
                + lep_p_max
                + ')(muons)',
            )
            .Define('n_selected_muons', 'ReconstructedParticle::get_n(selected_muons)')
            # select electrons based on p
            .Define(
                'selected_electrons',
                'ReconstructedParticle::sel_p('
                + lep_p_min
                + ','
                + lep_p_max
                + ')(electrons)',
            )
            .Define(
                'n_selected_electrons',
                'ReconstructedParticle::get_n(selected_electrons)',
            )
            # merge selected electrons and muons
            .Define(
                'selected_leptons',
                'ReconstructedParticle::merge(selected_electrons, selected_muons)',
            )
            # find Z leptons (only best Z->ll candidate: same flavour,
            # opposite sign, mass closest to mZ)
            .Define(
                'zed_leptons', 'ReconstructedParticle::findZleptons(selected_leptons)'
            )
            .Define('n_zed_leptons', 'ReconstructedParticle::get_n(zed_leptons)')
            .Define('zed_leptons_p', 'ReconstructedParticle::get_p(zed_leptons)')
            .Define(
                'zed_leptons_theta', 'ReconstructedParticle::get_theta(zed_leptons)'
            )
            .Define('zed_leptons_e', 'ReconstructedParticle::get_e(zed_leptons)')
            .Define('zed_leptons_phi', 'ReconstructedParticle::get_phi(zed_leptons)')
            .Define('zed_leptons_m', 'ReconstructedParticle::get_mass(zed_leptons)')
            .Define('zed_leptons_tlv', 'ReconstructedParticle::get_tlv(zed_leptons)')
            # Remove Z leptons from selected leptons
            # In the past it was isoleptons and extraisoleptons but I don't have isolated
            # leptons from Delphes anymore
            .Define(
                'extraleptons',
                'ReconstructedParticle::remove(selected_leptons,zed_leptons)',
            )
            .Define('n_extraleptons', 'ReconstructedParticle::get_n(extraleptons)')
            .Define('extraleptons_p', 'ReconstructedParticle::get_p(extraleptons)')
            .Define(
                'extraelectrons',
                'ReconstructedParticle::remove(selected_electrons,zed_leptons)',
            )
            .Define('n_extraelectrons', 'ReconstructedParticle::get_n(extraelectrons)')
            .Define('extraelectrons_p', 'ReconstructedParticle::get_p(extraelectrons)')
            .Define(
                'extramuons',
                'ReconstructedParticle::remove(selected_muons,zed_leptons)',
            )
            .Define('n_extramuons', 'ReconstructedParticle::get_n(extramuons)')
            .Define('extramuons_p', 'ReconstructedParticle::get_p(extramuons)')
            # to suppress H(tautau) and H(VV) semileptonic also look at all leptons since
            # momentum spectrum could be softer
            .Define(
                'allextraleptons', 'ReconstructedParticle::remove(leptons,zed_leptons)'
            )
            .Define(
                'n_allextraleptons', 'ReconstructedParticle::get_n(allextraleptons)'
            )
            .Define(
                'allextraleptons_p', 'ReconstructedParticle::get_p(allextraleptons)'
            )
            .Define('maxplep', 'Utils::getmax(allextraleptons_p)*(n_allextraleptons>0)')
            # build the Z candidate
            # note: flavour of Z can be determined as follows:
            # n_selected_electrons - n_extraelectrons == 2 => Z->ee
            # n_selected_muons - n_extramuons == 2 => Z->mumu
            .Define(
                'zed_leptonic',
                'ReconstructedParticle::resonanceBuilder(91.2)(zed_leptons)',
            )
            .Define(
                'zed_leptonic_flavour',
                '(n_selected_electrons-n_extraelectrons)/2+(n_selected_muons-n_extramuons)',
            )
            .Define('zed_leptonic_p', 'ReconstructedParticle::get_p(zed_leptonic)[0]')
            .Define(
                'zed_leptonic_m', 'ReconstructedParticle::get_mass(zed_leptonic)[0]'
            )
            .Define(
                'zed_leptonic_theta',
                'ReconstructedParticle::get_theta(zed_leptonic)[0]',
            )
            .Define(
                'zed_leptonic_phi', 'ReconstructedParticle::get_phi(zed_leptonic)[0]'
            )
            # useless, 0 by construction
            .Define(
                'zed_leptonic_charge',
                'ReconstructedParticle::get_charge(zed_leptonic)[0]',
            )
            # useful for plots/selection
            .Define(
                'zed_leptonic_cos_theta',
                'abs(cos(ReconstructedParticle::get_theta(zed_leptonic)[0]))',
            )
            # calculate recoil of the Z
            .Define(
                'zed_leptonic_recoil',
                'ReconstructedParticle::recoilBuilder(365)(zed_leptonic)',
            )
            .Define(
                'zed_leptonic_recoil_m',
                'ReconstructedParticle::get_mass(zed_leptonic_recoil)[0]',
            )
            # .Define(
            #     'zed_leptons_idx',
            #     'ReconstructedParticle::get_idx(ReconstructedParticles,zed_leptons)',
            # )
            # Define the px, py, pz and m of the particles to cluster - removing the Z leptons
            .Define(
                'MyReconstructedParticles',
                'ReconstructedParticle::remove(ReconstructedParticles, zed_leptons)',
            )
        )

        # DO JET CLUSTERING AND FLAVOUR TAGGING
        njets = 2
        tag = ''
        collections = {
            'GenParticles': 'Particle',
            'PFParticles': 'MyReconstructedParticles',
            'PFTracks': 'EFlowTrack',
            'PFPhotons': 'EFlowPhoton',
            'PFNeutralHadrons': 'EFlowNeutralHadron',
            'TrackState': 'EFlowTrack_1',
            'TrackerHits': 'TrackerHits',
            'CalorimeterHits': 'CalorimeterHits',
            'dNdx': 'EFlowTrack_2',
            'PathLength': 'EFlowTrack_L',
            'Bz': 'magFieldBz',
        }

        # define jet clustering parameters
        jetClusteringHelper = ExclusiveJetClusteringHelper(
            collections['PFParticles'], njets, tag
        )

        # run jet clustering
        df2 = jetClusteringHelper.define(df2)

        # define jet flavour tagging parameters
        jetFlavourHelper = JetFlavourHelper(
            collections,
            jetClusteringHelper.jets,
            jetClusteringHelper.constituents,
            tag,
        )

        # define observables for tagger
        df2 = jetFlavourHelper.define(df2)

        # run tagger inference
        df2 = jetFlavourHelper.inference(weaver_preproc, weaver_model, df2)


        # CALCULATE REMAINING VARIABLES
        df3 = (
            df2
            .Define('event_d23', 'JetClusteringUtils::get_exclusive_dmerge(_jet, 2)')
            .Define('event_d34', 'JetClusteringUtils::get_exclusive_dmerge(_jet, 3)')
            .Define('event_d45', 'JetClusteringUtils::get_exclusive_dmerge(_jet, 4)')
            # get truth jet flavour
            .Define(
                'jet_flavour', 'JetTaggingUtils::get_flavour(jet, Particle, 2, 0.8)'
            )
            .Define(
                'selected_jets',
                'JetClusteringUtils::sel_p(' + jet_p_min + ',' + jet_p_max + ')(jet)',
            )
            .Define('n_selected_jets', 'JetClusteringUtils::get_n(selected_jets)')
            .Define('selected_jets_pt', 'JetClusteringUtils::get_pt(selected_jets)')
            .Define('selected_jets_eta', 'JetClusteringUtils::get_eta(selected_jets)')
            .Define('selected_jets_p', 'JetClusteringUtils::get_p(selected_jets)')
            .Define('selected_jets_m', 'JetClusteringUtils::get_m(selected_jets)')
            # H->two selected jets (only those passing certain p cut)
            .Define(
                'higgs_hadronic',
                'ReconstructedParticle::jetResonanceBuilder(125)(selected_jets)',
            )
            .Define(
                'higgs_hadronic_m', 'ReconstructedParticle::get_mass(higgs_hadronic)[0]'
            )
            .Define(
                'higgs_hadronic_p', 'ReconstructedParticle::get_p(higgs_hadronic)[0]'
            )
            # H->two jets, no p cut
            # .Define('higgs_hadronic_2', 'ReconstructedParticle::multijetResonanceBuilder(125)(jets)')
            .Define(
                'higgs_hadronic_2',
                'ReconstructedParticle::jetResonanceBuilder(125,1)(jet)',
            )
            .Define(
                'higgs_hadronic_m_2',
                'ReconstructedParticle::get_mass(higgs_hadronic_2)[0]',
            )
            .Define(
                'higgs_hadronic_p_2',
                'ReconstructedParticle::get_p(higgs_hadronic_2)[0]',
            )
            #
            # pmiss
            #
            # create branch with etmiss (despite the name it's actually
            # the missing momentum
            .Define('etmiss', 'MissingET.energy[0]')
        )

        # get flavour tagging information

        df3 = (
            df3.Define('jet1_E', 'jet_e[0]')
            .Define('jet2_E', 'jet_e[1]')
            .Define('jet1_nconst', 'jet_nconst[0]')
            .Define('jet2_nconst', 'jet_nconst[1]')
            .Define('jet1_isB', 'recojet_isB[0]')
            .Define('jet1_isC', 'recojet_isC[0]')
            .Define('jet1_isS', 'recojet_isS[0]')
            # .Define('jet1_isQ', 'recojet_isQ[0]')
            .Define('jet1_isU', 'recojet_isU[0]')
            .Define('jet1_isD', 'recojet_isD[0]')
            .Define('jet1_isTAU', 'recojet_isTAU[0]')
            .Define('jet1_isG', 'recojet_isG[0]')
            .Define('jet2_isB', 'recojet_isB[1]')
            .Define('jet2_isC', 'recojet_isC[1]')
            .Define('jet2_isS', 'recojet_isS[1]')
            # .Define('jet2_isQ', 'recojet_isQ[1]')
            .Define('jet2_isU', 'recojet_isU[1]')
            .Define('jet2_isD', 'recojet_isD[1]')
            .Define('jet2_isTAU', 'recojet_isTAU[1]')
            .Define('jet2_isG', 'recojet_isG[1]')
        )

        return df3

    # __________________________________________________________
    # SAVE PREDICTIONS & OBSERVABLES FOR ANALYSIS
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            # MC truth
            'MC_HiggsDecay',
            # all leptons
            'n_all_electrons',
            'n_all_muons',
            'n_all_leptons',
            'n_iso_leptons',
            'leptons_p',
            'leptons_iso',
            'isolated_leptons_p',
            'isolated_leptons_pmax',
            # selected leptons
            'n_selected_electrons',
            'n_selected_muons',
            'n_zed_leptons',
            'zed_leptons_p',
            #'zed_leptons_cos_theta',
            'zed_leptons_theta',
            'zed_leptons_phi',
            'zed_leptons_e',
            'zed_leptons_m',
            # extra leptons (was isolated leptons before..)
            'n_extraelectrons',
            'n_extramuons',
            'n_extraleptons',
            'n_allextraleptons',
            'extraleptons_p',
            'extraelectrons_p',
            'extramuons_p',
            'allextraleptons_p',
            'maxplep',
            # Z->selected leptons
            'zed_leptonic_flavour',
            'zed_leptonic_p',
            'zed_leptonic_cos_theta',
            'zed_leptonic_theta',
            'zed_leptonic_phi',
            'zed_leptonic_m',
            'zed_leptonic_charge',
            # recoil mass
            'zed_leptonic_recoil_m',
        ]
        branchList += jetClusteringHelper.outputBranches()
        branchList += [
            # in my code event_dxx were added by jetClusteringHelper.. compare!
            'event_d23',
            'event_d34',
            'event_d45',
            'jet_flavour',
            'jet1_E',
            'jet1_nconst',
            'jet1_isB',
            'jet1_isC',
            'jet1_isS',
            # 'jet1_isQ',
            'jet1_isU',
            'jet1_isD',
            'jet1_isTAU',
            'jet1_isG',
            'jet2_E',
            'jet2_nconst',
            'jet2_isB',
            'jet2_isC',
            'jet2_isS',
            # 'jet2_isQ',
            'jet2_isU',
            'jet2_isD',
            'jet2_isTAU',
            'jet2_isG',
            'n_selected_jets',
            'selected_jets_p',
            'selected_jets_pt',
            'selected_jets_eta',
            'selected_jets_m',
            'higgs_hadronic_m',
            'higgs_hadronic_p',
            'higgs_hadronic_m_2',
            'higgs_hadronic_p_2',
            'etmiss',
        ]
        return branchList
