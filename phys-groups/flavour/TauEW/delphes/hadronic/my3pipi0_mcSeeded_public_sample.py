import ROOT

##################################################################################################
# Load custom C-functions
##################################################################################################
#ROOT.gInterpreter.Declare('#include "my_analysis.cpp"')

processList = {
    "p8_ee_Ztautau_ecm91": {}, # USE THIS LINE WHEN YOU WANT TO RUN OVER THE COMPLETE SAMPLE
    #"events_164192792": {}, # USE THIS LINE TO ONLY RUN ABOUT THIS SUBSET OF THE WHOLE SAMPLE
    #"events_198604879": {},
}

includePaths = ["analyzers_Tau3PiPi0.h"]

inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA" # Whole sample
#inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Ztautau_ecm91" # Subset of the sample
#inputDir    = "/afs/cern.ch/user/a/aumarten/work/fcc/samples"
outputDir   = "result_3pipi0"

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
            .Filter("0 < rdfentry_ && rdfentry_<= 100000000000") # USE EVEN SMALLER SUBSET OF THE SAMPLE (FAST CODE TESTING)
            
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
            .Define("MCtau3pipi0nu_indices",
            "MCParticle::get_indices(15, {-211,211,-211,22,22,16}, true, true, true, false) (Particle, Daughters)")

            # select events for which the requested decay chain has been found:
            .Filter("MCtau3pipi0nu_indices.size() > 0")
            
            # the tau :
            .Define("MC_tau", "return Particle.at(MCtau3pipi0nu_indices[0]);")
            .Define("MC_Pion1", "return Particle.at(MCtau3pipi0nu_indices[1]);")
            .Define("MC_tau3pi_invMass", "VtxAna::tau3pipi0_MC_mass(MCtau3pipi0nu_indices,Particle)")
            # Decay vertex (an `edm4hep::Vector3d`) of the tau (MC) = production
            # vertex of the muplus:
            .Define("TauMCDecayVertex", "return MC_Pion1.vertex;")
            .Define("TauMCDecayVertex_x", "return TauMCDecayVertex.x")
            .Define("TauMCDecayVertex_y", "return TauMCDecayVertex.y")
            .Define("TauMCDecayVertex_z", "return TauMCDecayVertex.z")

            .Alias("RecoIndex", "MCRecoAssociations#0.index") # Points to RecoParticles
            .Alias("MCIndex", "MCRecoAssociations#1.index") # Points to MCParticles
        
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
            
            #empty
            #.Define("MCTauMinus_dvx","MCParticle::get_endPoint_x(MC_tau1)[0]")
            #.Define("MCTauMinus_dvy","MCParticle::get_endPoint_y(MC_tau1)[0]")
            #.Define("MCTauMinus_dvz","MCParticle::get_endPoint_z(MC_tau1)[0]")

            .Define("MCTauPlus_px","MCParticle::get_px(MC_tau2)[0]")
            .Define("MCTauPlus_py","MCParticle::get_py(MC_tau2)[0]")
            .Define("MCTauPlus_pz","MCParticle::get_pz(MC_tau2)[0]")
            .Define("MCTauPlus_E","MCParticle::get_e(MC_tau2)[0]")
            
            #empty
            #.Define("MCTauPlus_dvx","MCParticle::get_endPoint_x(MC_tau2)[0]")
            #.Define("MCTauPlus_dvy","MCParticle::get_endPoint_y(MC_tau2)[0]")
            #.Define("MCTauPlus_dvz","MCParticle::get_endPoint_z(MC_tau2)[0]")
        )
        print(f"MC Tau^- --> pi^- pi^+ pi^- pi^0 nu_tau and CC : {dframe0.Count().GetValue()}")
        RDFanalysis.output_var.extend(["MCTauMinus_px","MCTauMinus_py","MCTauMinus_pz","MCTauMinus_E"])
        RDFanalysis.output_var.extend(["MCTauPlus_px","MCTauPlus_py","MCTauPlus_pz","MCTauPlus_E"])
        RDFanalysis.output_var.extend(["TauMCDecayVertex_x","TauMCDecayVertex_y","TauMCDecayVertex_z","MC_tau3pi_invMass"])

        ##################################################################################################
        # Reconstructed Kinematics: MC seeded
        ##################################################################################################
        dframe2 = (
            # Returns the RecoParticles associated with the tau decay products.
            # The size of this collection is always 4 provided that
            # MCtau3pinu_indices is not empty, possibly including "dummy"
            # particles in case one of the legs did not make a RecoParticle
            # (e.g. because it is outside the tracker acceptance). This is done
            # on purpose, in order to maintain the mapping with the indices ---
            # i.e. the 1st particle in the list MCtau3pinu_indices is the pi-,
            # , etc.
            # (selRP_matched_to_list ignores the unstable MC particles that are
            # in the input list of indices hence the mother particle, which is
            # the [0] element of the MCtau3pinu_indices vector).
            #
            # The matching between RecoParticles and MCParticles requires 4
            # collections. For more detail, see
            # https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics
            dframe0.Define("TauRecoParticles",
                    "ReconstructedParticle2MC::selRP_matched_to_list(MCtau3pipi0nu_indices, RecoIndex, MCIndex, ReconstructedParticles, Particle)")
            
            # the corresponding tracks --- here, dummy particles, if any, are
            # removed, i.e. one may have < 4 tracks, e.g. if one muon or kaon
            # was emitted outside of the acceptance
            .Define("TauTracks",
                    "ReconstructedParticle2Track::getRP2TRK(TauRecoParticles, EFlowTrack_1)")
                    
            # number of tracks in this TauTracks collection (= the #tracks
            # used to reconstruct the Tau vertex)
            .Define("n_TauTracks",
                    "ReconstructedParticle2Track::getTK_n(TauTracks)")
                    
            # number of tracks in this BsTracks collection (= the #tracks
            # used to reconstruct the Bs vertex)
            .Filter("n_TauTracks==3")
                    
            # Fit the tracks to a common vertex. That would be a secondary
            # vertex, hence we put a "2" as the first argument of
            # VertexFitter_Tk: First the full object, of type
            # Vertexing::FCCAnalysesVertex
            .Define("TauVertexObject", "VertexFitterSimple::VertexFitter_Tk(2, TauTracks)")
            # from which we extract the edm4hep::VertexData object, which
            # contains the vertex position in mm
            .Define("TauVertex",
                    "VertexingUtils::get_VertexData(TauVertexObject)")
            .Define("TauVertex_chi2","TauVertex.chi2")
            .Define("TauVertex_x","TauVertex.position.x")
            .Define("TauVertex_y","TauVertex.position.y")
            .Define("TauVertex_z","TauVertex.position.z")
            .Define("TauVertexCharge",
                    "Sum(ReconstructedParticle::get_charge(TauRecoParticles))")
            #.Define("TauVertex_ndf","TauVertex.ndf")
            # The reco'ed tau mass --- from the post-VertxFit momenta, at the
            # tau decay vertex:
            .Define("invMass_3pi_fit", "VtxAna::tau3pi_vertex_mass(TauVertexObject)")
            # The "raw" mass --- using the track momenta at their dca:
            .Define("invMass_3pipi0_raw", "VtxAna::tau3pipi0_raw_mass(TauRecoParticles)")
                    
            #.Define('RP_MC_index', "ReconstructedParticle2MC::getRP2MC_index(RecoIndex,MCIndex,ReconstructedParticles)")
        
        )
        print(f"Reco-ed tau->3pipi0 (mc-seeded): {dframe2.Count().GetValue()}")
        RDFanalysis.output_var.extend(["invMass_3pi_fit","invMass_3pipi0_raw","TauVertex_chi2","TauVertex_x","TauVertex_y","TauVertex_z","TauVertexCharge",])
        
        print("Analysis done :)")
        return dframe2


    def output():
        '''
        Output variables which will be saved to output root file.
        '''

        branch_list=RDFanalysis.output_var

        return branch_list
    
