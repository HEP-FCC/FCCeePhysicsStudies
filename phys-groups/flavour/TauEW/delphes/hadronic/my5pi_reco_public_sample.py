import ROOT

##################################################################################################
# Load custom C-functions
##################################################################################################
#ROOT.gInterpreter.Declare('#include "my_analysis.cpp"')

processList = {
    #"p8_ee_Ztautau_ecm91": {}, # USE THIS LINE WHEN YOU WANT TO RUN OVER THE COMPLETE SAMPLE
    #"p8_ee_Zcc_ecm91": {}, #ccbar
    "p8_ee_Zbb_ecm91": {}, #bbbar
    "p8_ee_Zss_ecm91": {}, #ssbar
    "p8_ee_Zud_ecm91": {}, #uu-ddbar
    #"events_164192792": {}, # USE THIS LINE TO ONLY RUN ABOUT THIS SUBSET OF THE WHOLE SAMPLE
    #"events_198604879": {},
}

includePaths = ["analyzers_Tau5Pi.h"]

inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA" # Whole sample
#inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Ztautau_ecm91" # Subset of the sample
#inputDir    = "/afs/cern.ch/user/a/aumarten/work/fcc/samples"
outputDir   = "result_5pireco"


class RDFanalysis():
    '''
    Mandatory class where the user defines the operations on the dataframe.
    '''

    def analysers(df):
        '''
        Mandatory function to define the actual analysers, please make sure
        you return the last dataframe, in this example it is df2.
        '''
        df2 = (
            df.Define("Reco_charge","ReconstructedParticle::get_charge(ReconstructedParticles)")
            .Define("RecoPionsC_indices", "VtxAna::getRecoIndices(1,true,0.139,ReconstructedParticles)")
            .Define("RecoPions", "ReconstructedParticle::get(RecoPionsC_indices,ReconstructedParticles)")
            .Define("nRecoPions", "return RecoPions.size()")
            # assume a leptonic tag for the tau event
            .Filter("nRecoPions==5") # Only keep events with exactly 5 reconstructed pions
            .Define("RecoPions_px","ReconstructedParticle::get_px(RecoPions)[0]")
            .Define("RecoPions_py","ReconstructedParticle::get_py(RecoPions)[0]")
            .Define("RecoPions_pz","ReconstructedParticle::get_pz(RecoPions)[0]")
            # Build multiplets of pions.
            .Define("multiplets", "VtxAna::build_multiplets(RecoPions, -1.,true)")
            .Define("n_multiplets", "return multiplets.size();")
            #.Filter("n_multiplets==1")
            .Define("multiplet_charge", "VtxAna::multiplet_charge(multiplets)")
            # count photons
            .Alias("Photon0","Photon#0.index")
            .Define("photons",
                    "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
            .Define("n_photons", "ReconstructedParticle::get_n(photons)")
            # count muons
            .Alias("Muon0","Muon#0.index")
            .Define("muons",
                    "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            .Define("n_muons", "ReconstructedParticle::get_n(muons)")
            .Define("muons_charge", "ReconstructedParticle::get_charge(muons)")
            # count electrons
            .Alias("Electron0","Electron#0.index")
            .Define("electrons",
                    "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
            .Define("n_electrons", "ReconstructedParticle::get_n(electrons)")
            .Define("electrons_charge", "ReconstructedParticle::get_charge(electrons)")
            # ----------------------------------------------------
            # Considering all multiplets:
            .Define("TauVertexObject",
                    "VtxAna::build_AllTauVertexObject(multiplets, EFlowTrack_1)")
            .Define("TauVertex",
                    "VertexingUtils::get_VertexData(TauVertexObject)")
            .Define("TauVertex_chi2","VertexingUtils::get_chi2_SV(TauVertexObject)")
            .Define("TauVertex_pos","VertexingUtils::get_position_SV(TauVertexObject)")
            .Define("TauVertex_x","myUtils::get_Vertex_x(TauVertexObject)")
            .Define("TauVertex_y","myUtils::get_Vertex_y(TauVertexObject)")
            .Define("TauVertex_z","myUtils::get_Vertex_z(TauVertexObject)")
            .Define("TauMass_allCandidates",
                    "VtxAna::build_AllTauMasses(TauVertexObject)")
        )
        return df2


    def output():
        '''
        Mandatory output function, please make sure you return the branch list
        (the list of dataframe columns to be saved).
        '''
        branchList = [
            "n_multiplets","n_photons","n_muons","n_electrons",
            "electrons_charge","muons_charge","multiplet_charge",
            "TauMass_allCandidates",
            "TauVertex_chi2","TauVertex_x","TauVertex_y","TauVertex_z"
        ]

        return branchList
