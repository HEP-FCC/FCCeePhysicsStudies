#ifndef FCCANA_ADDITIONAL_ANALYZERS_H
#define FCCANA_ADDITIONAL_ANALYZERS_H

// C++ standard library
#include <cmath>
#include <random>
#include <chrono>

// ROOT
#include "TLorentzVector.h"
#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/VertexData.h"
#include "edm4hep/MCParticleData.h"

// FCCAnalyses
#include "FCCAnalyses/VertexingUtils.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexFitterSimple.h"

namespace FCCAnalyses :: VtxAna {
  const double PION_MASS = 0.13957;  // GeV
  const double PI0_MASS = 0.13498;  // GeV

 // double vertex_chi2(const edm4hep::VertexData& vertex) {
 //   return vertex.chi2;
 // }

//int vertex_ndf(const edm4hep::VertexData& vertex) {
//    return vertex.ndf;
//  }

  double tau3pi_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex) {
    TLorentzVector tau;
    ROOT::VecOps::RVec<TVector3> momenta = vertex.updated_track_momentum_at_vertex;
    int n = momenta.size();
    if (n!=3)
      cout << n << endl;
    for (int ileg=0; ileg < n; ileg++) {
      TVector3 track_momentum = momenta[ileg];
      TLorentzVector leg;
      leg.SetXYZM(track_momentum[0], track_momentum[1], track_momentum[2], PION_MASS) ;
      tau += leg;
    }

    return tau.M();
  }

  double tau3pipi0_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& legs) {
    TLorentzVector tau;
    int n = legs.size();
    //cout << n << endl;
    for (int ileg=0; ileg < 3; ileg++) {
      TLorentzVector leg;
      leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, PION_MASS);
      tau += leg;
    }
    // add photons
    for (int ileg=3; ileg < 5; ileg++) {
      TLorentzVector leg;
      leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z,0.);
      tau += leg;
    }
    
    return tau.M();
  }

 double tau3pipi0_MC_mass(const ROOT::VecOps::RVec< int >& indices,const ROOT::VecOps::RVec<edm4hep::MCParticleData>& parts) {
   ROOT::Math::PxPyPzMVector tau;
   for (int ileg=0;ileg<5;ileg++) {
     ROOT::Math::PxPyPzMVector leg;
     edm4hep::MCParticleData part = parts.at(indices[ileg+1]);
     leg.SetCoordinates(part.momentum.x,part.momentum.y,part.momentum.z,part.mass);
     tau += leg;
   }
  return tau.M();
 }

ROOT::VecOps::RVec<int> getRecoIndices(const double charge, const bool conj, double mass, const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& recoParticle) {
    ROOT::VecOps::RVec<int> indices;
    ROOT::VecOps::RVec< double > c = FCCAnalyses::ReconstructedParticle::get_charge(recoParticle);
    ROOT::VecOps::RVec< double > m = FCCAnalyses::ReconstructedParticle::get_mass(recoParticle);
    double tol = 0.001;

    for (int i = 0; i < m.size(); i++) {
        if (c[i] == charge) {
            if ( m[i] < mass+tol && m[i] > mass-tol) {
                indices.push_back(i);
            }
        }
        else if (c[i] == charge*-1 && conj==true) {
            if ( m[i] < mass+tol && m[i] > mass-tol) {
                indices.push_back(i);
            }
        }
    }
    return indices;
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>
build_triplets(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles,
               float total_charge, bool conj) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

  int n = inParticles.size();
  if (n < 3) {
    return result;
  }

  for (int i = 0; i < n; ++i) {
    edm4hep::ReconstructedParticleData pi = inParticles[i];

    for (int j = i + 1; j < n; ++j) {
      edm4hep::ReconstructedParticleData pj = inParticles[j];

      for (int k=j+1; k < n; ++k) {
        edm4hep::ReconstructedParticleData pk = inParticles[k];
        float charge_tot = pi.charge + pj.charge + pk.charge;

        if ( (charge_tot == total_charge) || (conj && (charge_tot == -total_charge)) ) {
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_triplet = {pi, pj, pk};
          result.push_back(a_triplet);
        }
      }  // end of the loop over k
    }  // end of the loop over j
  }  // end of the loop over i

  return result;
}

ROOT::VecOps::RVec<float>
triplet_charge(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& triplets) {
  ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex> results;
  int ntriplets = triplets.size();
  ROOT::VecOps::RVec<float> tot_charge;
  for (int i=0; i < ntriplets; i++) {
    float charge= 0;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = triplets[i];
    for (int k=0;k<legs.size();k++)
      charge += legs[k].charge;
    tot_charge.push_back(charge);
  }

  return tot_charge;
}

float
diphoton_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& pi0) {
  TLorentzVector p4 = ReconstructedParticle::get_P4vis(pi0);
  return p4.M();
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>
build_diphotons(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles,const float mMin, const float mMax) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

  int n = inParticles.size();
  if (n < 2) {
    return result;
  }

  for (int i = 0; i < n; ++i) {
    edm4hep::ReconstructedParticleData pi = inParticles[i];

    for (int j = i + 1; j < n; ++j) {
      edm4hep::ReconstructedParticleData pj = inParticles[j];
      
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_pi0 = {pi, pj};
      
      // filter mass range
      auto mass = diphoton_mass(a_pi0);
      if (mass>mMin && mass<mMax)
        result.push_back(a_pi0);
    }  // end of the loop over j
  }  // end of the loop over i

  return result;
}

ROOT::VecOps::RVec<TLorentzVector>
diphoton_p4vis(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& pi0s) {
  int npi0s = pi0s.size();
  ROOT::VecOps::RVec<TLorentzVector> tot_p4;
  for (int i=0; i < npi0s; i++) {
    TLorentzVector p4 = ReconstructedParticle::get_P4vis(pi0s[i]);
    tot_p4.push_back(p4);
  }
  return tot_p4;
}



ROOT::VecOps::RVec<float>
p4_mass(const ROOT::VecOps::RVec<TLorentzVector>& p4s) {
  int npi0s = p4s.size();
  ROOT::VecOps::RVec<float> tot_mass;
  for (int i=0; i < npi0s; i++) {
    float val = p4s[i].M();
    tot_mass.push_back(val);
  }
  return tot_mass;
}

ROOT::VecOps::RVec<float>
p4_px(const ROOT::VecOps::RVec<TLorentzVector>& p4s) {
  int npi0s = p4s.size();
  ROOT::VecOps::RVec<float> tot_mass;
  for (int i=0; i < npi0s; i++) {
    float val = p4s[i].Px();
    tot_mass.push_back(val);
  }
  return tot_mass;
}

ROOT::VecOps::RVec<float>
p4_py(const ROOT::VecOps::RVec<TLorentzVector>& p4s) {
  int npi0s = p4s.size();
  ROOT::VecOps::RVec<float> tot_mass;
  for (int i=0; i < npi0s; i++) {
    float val = p4s[i].Py();
    tot_mass.push_back(val);
  }
  return tot_mass;
}

ROOT::VecOps::RVec<float>
p4_pz(const ROOT::VecOps::RVec<TLorentzVector>& p4s) {
  int npi0s = p4s.size();
  ROOT::VecOps::RVec<float> tot_mass;
  for (int i=0; i < npi0s; i++) {
    float val = p4s[i].Pz();
    tot_mass.push_back(val);
  }
  return tot_mass;
}

ROOT::VecOps::RVec<float>
p4_pt(const ROOT::VecOps::RVec<TLorentzVector>& p4s) {
  int npi0s = p4s.size();
  ROOT::VecOps::RVec<float> tot_mass;
  for (int i=0; i < npi0s; i++) {
    float val = p4s[i].Pt();
    tot_mass.push_back(val);
  }
  return tot_mass;
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>
build_taus(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& pi0s,const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& hadtracks, const int npi0pairs) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

  if (npi0pairs>1) {
    cout << "VtxAna ERROR : number of requested pi0s pairs is not implemented: " << npi0pairs << " >1. Please implement code to improve." << endl;
    return result;
  }
  
  int npi0s = pi0s.size();
  if (npi0s < npi0pairs) {
    return result;
  }
  
  int nhads = hadtracks.size();
  if (nhads < 1) {
    return result;
  }

  for (int i = 0; i < nhads; ++i) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pi = hadtracks[i];
    if (pi.size()==3) {
      for (int j = 0; j < npi0s; ++j) {
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pj = pi0s[j];
        if (pj.size()==2) {
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_tau = {pi[0], pi[1],pi[2], pj[0],pj[1]};
          result.push_back(a_tau);
        }
      }  // end of the loop over j
    }
  }  // end of the loop over i

  return result;
}

ROOT::VecOps::RVec<TLorentzVector>
taus_p4vis(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& taus) {
  int ntaus = taus.size();
  ROOT::VecOps::RVec<TLorentzVector> tot_p4;
  for (int i=0; i < ntaus; i++) {
    TLorentzVector p4 = ReconstructedParticle::get_P4vis(taus[i]);
    tot_p4.push_back(p4);
  }
  return tot_p4;
}

ROOT::VecOps::RVec<TLorentzVector>
etas_p4vis(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& etas) {
  int netas = etas.size();
  ROOT::VecOps::RVec<TLorentzVector> tot_p4;
  for (int i=0; i < netas; i++) {
    TLorentzVector p4 = ReconstructedParticle::get_P4vis(etas[i]);
    tot_p4.push_back(p4);
  }
  return tot_p4;
}

float
eta_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& eta) {
  TLorentzVector p4 = ReconstructedParticle::get_P4vis(eta);
  return p4.M();
}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>
build_etas(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& pi0s,const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& hadtracks, const int npi0pairs, const float mMin, const float mMax) {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

  if (npi0pairs>1) {
    cout << "VtxAna ERROR in build_etas : number of requested pi0s pairs is not implemented: " << npi0pairs << " >1. Please implement code to improve." << endl;
    return result;
  }
  
  int npi0s = pi0s.size();
  if (npi0s < npi0pairs) {
    return result;
  }
  
  int nhads = hadtracks.size();
  if (nhads < 1) {
    return result;
  }

  for (int i = 0; i < nhads; ++i) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pi = hadtracks[i];
    if (pi.size()==3) {
      for (int j = 0; j < npi0s; ++j) {
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pj = pi0s[j];
        if (pj.size()==2) {
          ROOT::VecOps::RVec<float> charges = ReconstructedParticle::get_charge(pi);
          if (charges[0]!=charges[1]) {
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_eta = {pi[0], pi[1], pj[0],pj[1]};
            auto mass = eta_mass(a_eta);
            if (mass>mMin && mass<mMax)
              result.push_back(a_eta);
          }
          if (charges[0]!=charges[2]) {
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_eta = {pi[0],pi[2],pj[0],pj[1]};
            auto mass = eta_mass(a_eta);
            if (mass>mMin && mass<mMax)
              result.push_back(a_eta);
          }
          if (charges[1]!=charges[2]) {
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_eta = {pi[1],pi[2],pj[0],pj[1]};
            auto mass = eta_mass(a_eta);
            if (mass>mMin && mass<mMax)
              result.push_back(a_eta);
          }
        }
      }  // end of the loop over j
    }
  }  // end of the loop over i

  return result;
}


  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>
  build_AllTauVertexObject(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& triplets,
                           const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks) {
    ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex> results;
    int ntriplets = triplets.size();
    for (int i=0; i < ntriplets; i++) {
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = triplets[i];

      ROOT::VecOps::RVec<edm4hep::TrackState> the_tracks = ReconstructedParticle2Track::getRP2TRK(legs, allTracks);
      VertexingUtils::FCCAnalysesVertex vertex = VertexFitterSimple::VertexFitter_Tk(2, the_tracks);
      results.push_back(vertex);
    }

    return results;
  }

  ROOT::VecOps::RVec<double>
  build_AllTauMasses(const ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>& vertices) {
    ROOT::VecOps::RVec<double> results;
    for (const auto& v: vertices) {
      double mass = tau3pi_vertex_mass(v);
      results.push_back(mass);
    }

    return results;
  }

  struct selRP_Fakes {
    selRP_Fakes(float arg_fakeRate, float arg_mass);

    float m_fakeRate = 1e-3;  // fake rate
    float m_mass = PION_MASS;  // particle mass
    std::default_random_engine m_generator;
    std::uniform_real_distribution<float> m_flat;

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles);
  };

  selRP_Fakes::selRP_Fakes(float arg_fakeRate, float arg_mass): m_fakeRate(arg_fakeRate),
                                                                m_mass(arg_mass) {
    auto seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);
    m_generator = generator;
    std::uniform_real_distribution<float> flatdis(0., 1.);
    m_flat.param(flatdis.param());
  };

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  selRP_Fakes::operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    for (const auto& p: inParticles) {
      float arandom = m_flat(m_generator);
      if (arandom <= m_fakeRate) {
        edm4hep::ReconstructedParticleData reso = p;
        // overwrite the mass:
        reso.mass = m_mass;
        result.push_back(reso);
      }
    }

    return result;
  }
}

#endif /* FCCANA_ADDITIONAL_ANALYZERS_H */
