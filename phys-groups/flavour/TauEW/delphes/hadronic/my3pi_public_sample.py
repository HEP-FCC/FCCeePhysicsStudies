import ROOT

##################################################################################################
# Load custom C-functions
##################################################################################################
ROOT.gInterpreter.Declare('#include "my_analysis.cpp"')

processList = {
    #"p8_ee_Ztautau_ecm91": {}, # USE THIS LINE WHEN YOU WANT TO RUN OVER THE COMPLETE SAMPLE
    "events_164192792": {}, # USE THIS LINE TO ONLY RUN ABOUT THIS SUBSET OF THE WHOLE SAMPLE
}     

#inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA" # Whole sample
inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Ztautau_ecm91" # Subset of the sample
outputDir   = "result"

##################################################################################################
# Main class of the Analysis
##################################################################################################
class RDFanalysis():
    output_var = []
    
    def analysers(dframe):
        ##################################################################################################
        # Set up MC_history collections
        ##################################################################################################
        dframe0 = (
            dframe
            .Filter("0 < rdfentry_ && rdfentry_<= 10000") # USE EVEN SMALLER SUBSET OF THE SAMPLE (FAST CODE TESTING)
            
            .Alias("Parents","Particle#0.index") # parents
            .Alias("Daughters","Particle#1.index") # daughters
            
            # MC indices of the decay
            # tau- (PDG = 15) -> pi- (PDG = -211) pi+ (PDG = 211) pi- (PDG = -211) nu_tau (16)
            # exclusive decay to remove events with additionnal pi0s, photons, other particles
            # Retrieves a vector of integers which correspond to indices in the
            # Particle block
            # vector[0] = the mother, and then the daughters in the order
            # specified, i.e. here [1] = the pi-, [2] = the pi+, [3] = the pi-,
            # [4] = the nu_tau
            #
            # Boolean arguments:
            #   1st: `stableDaughters`, when set to true, the daughters specified
            #        in the list are looked for among the final, stable
            #        particles that come out from the mother, i.e. the decay
            #        tree is explored recursively if needed.
            #   2nd: `chargeConjugateMother`
            #   3rd: `chargeConjugateDaughters`
            #   4th: `inclusiveDecay`, when set to false, if a mother is found,
            #        that decays into the particles specified in the list plus
            #        other particle(s), this decay is not selected.
            # If the event contains more than one such decays, only the first
            # one is kept.
            .Define("MCtau3pinu_indices",
            "MCParticle::get_indices(15, {-211,211,-211,16}, true, true, true, false) (Particle, Daughters)")

            # select events for which the requested decay chain has been found:
            .Filter("MCtau3pinu_indices.size() > 0")

            .Alias("RecoIndex", "MCRecoAssociations#0.index") # Points to RecoParticles
            .Alias("MCIndex", "MCRecoAssociations#1.index") # Points to MCParticles
            
            .Define('RP_MC_index', "ReconstructedParticle2MC::getRP2MC_index(RecoIndex,MCIndex,ReconstructedParticles)")
        )

        ##################################################################################################
        # MC-Kinematics and parents of both: Tau^+ and Tau^-
        ##################################################################################################
        dframe0 = (
            dframe0
            .Define("MC_tau1","MCParticle::sel_pdgID(15,false)(Particle)")
            .Define("MC_tau2","MCParticle::sel_pdgID(-15,false)(Particle)")

            .Define("MC_tau_parent", "MCParticle::get_leptons_origin(MC_tau1,Particle,Parents)")
            .Redefine("MC_tau1","MC_tau1[MC_tau_parent==23]")

            .Define("MC_tau_parent2", "MCParticle::get_leptons_origin(MC_tau2,Particle,Parents)")
            .Redefine("MC_tau2","MC_tau2[MC_tau_parent2==23]")

            .Define("MCTauMinus_px","MCParticle::get_px(MC_tau1)[0]")
            .Define("MCTauMinus_py","MCParticle::get_py(MC_tau1)[0]")
            .Define("MCTauMinus_pz","MCParticle::get_pz(MC_tau1)[0]")
            .Define("MCTauMinus_E","MCParticle::get_e(MC_tau1)[0]")

            .Define("MCTauPlus_px","MCParticle::get_px(MC_tau2)[0]")
            .Define("MCTauPlus_py","MCParticle::get_py(MC_tau2)[0]")
            .Define("MCTauPlus_pz","MCParticle::get_pz(MC_tau2)[0]")
            .Define("MCTauPlus_E","MCParticle::get_e(MC_tau2)[0]")
        )
        print(f"Entries begin: {dframe0.Count().GetValue()}")
        RDFanalysis.output_var.extend(["MCTauMinus_px","MCTauMinus_py","MCTauMinus_pz","MCTauMinus_E"])


        ##################################################################################################
        # Reconstructed Kinematics: Ask for exactly 3 reconstructed pions (One tau decays 3prong, one to leptonic)
        ##################################################################################################
        dframe2 = (
            dframe0
            .Define("Reco_charge","ReconstructedParticle::get_charge(ReconstructedParticles)")
            .Define("Reco_type","ReconstructedParticle::get_type(ReconstructedParticles)")
            .Define('RecoPionsC_indizes', "getRecoIndices(1,true,0.139,ReconstructedParticles)") # Function defined in .cpp file
            .Define('RecoPionsC', 'ReconstructedParticle::get(RecoPionsC_indizes,ReconstructedParticles)') 
            .Filter("RecoPionsC.size()==3") # Only keep events with exactly 3 reconstructed pions

            .Define("RecoPionsC_px","ReconstructedParticle::get_px(RecoPionsC)[0]")
            .Define("RecoPionsC_py","ReconstructedParticle::get_py(RecoPionsC)[0]")
            .Define("RecoPionsC_pz","ReconstructedParticle::get_pz(RecoPionsC)[0]")
            .Define("RecoPionsC_E","ReconstructedParticle::get_e(RecoPionsC)[0]")
        )
        print(f"Entries with 3 pions: {dframe2.Count().GetValue()}")
        RDFanalysis.output_var.extend(["Reco_type","RecoPionsC_px","RecoPionsC_py","RecoPionsC_pz"])

        ##################################################################################################
        # Vertex Reconstruction of 3 prong tau candidates using pion tracks
        ##################################################################################################
        dframe2 = ( 
            dframe2
            .Define("PionTracks", "ReconstructedParticle2Track::getRP2TRK( RecoPionsC, EFlowTrack_1)" )
            .Define("TauCandVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, PionTracks)" )
            .Define("TauCandVertex",  "VertexingUtils::get_VertexData( TauCandVertexObject)")
            .Define("TauCandVertex_x", "TauCandVertex.position.x")
            .Define("TauCandVertex_y", "TauCandVertex.position.y")
            .Define("TauCandVertex_z", "TauCandVertex.position.z")
        )
        RDFanalysis.output_var.extend(["TauCandVertex_x","TauCandVertex_y","TauCandVertex_z"])
        
        print("Analysis done :)")
        return dframe2


    def output():
        '''
        Output variables which will be saved to output root file.
        '''

        branch_list=RDFanalysis.output_var

        return branch_list
    
