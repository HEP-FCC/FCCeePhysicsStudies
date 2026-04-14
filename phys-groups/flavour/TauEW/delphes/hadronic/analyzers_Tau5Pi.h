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

  const int nPions = 5;

 // double vertex_chi2(const edm4hep::VertexData& vertex) {
 //   return vertex.chi2;
 // }

//int vertex_ndf(const edm4hep::VertexData& vertex) {
//    return vertex.ndf;
//  }

  double tau5pi_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex) {
    TLorentzVector tau;
    ROOT::VecOps::RVec<TVector3> momenta = vertex.updated_track_momentum_at_vertex;
    int n = momenta.size();
    if (n!=nPions)
      cout << n << endl;
    for (int ileg=0; ileg < n; ileg++) {
      TVector3 track_momentum = momenta[ileg];
      TLorentzVector leg;
      leg.SetXYZM(track_momentum[0], track_momentum[1], track_momentum[2], PION_MASS) ;
      tau += leg;
    }

    return tau.M();
  }

  double tau5pi_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& legs) {
    TLorentzVector tau;
    int n = legs.size();
    //cout << n << endl;
    for (int ileg=0; ileg < nPions; ileg++) {
      TLorentzVector leg;
      leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, PION_MASS);
      tau += leg;
    }

    return tau.M();
  }

 double tau5pi_MC_mass(const ROOT::VecOps::RVec< int >& indices,const ROOT::VecOps::RVec<edm4hep::MCParticleData>& parts) {
   ROOT::Math::PxPyPzMVector tau;
   for (int ileg=0;ileg<nPions;ileg++) {
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
  build_multiplets(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles,
                 float total_charge, bool conj) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

    int n = inParticles.size();
    if (n < nPions) {
      return result;
    }

    for (int i = 0; i < n; ++i) {
      edm4hep::ReconstructedParticleData pi = inParticles[i];

      for (int j = i + 1; j < n; ++j) {
        edm4hep::ReconstructedParticleData pj = inParticles[j];

        for (int k=j+1; k < n; ++k) {
          edm4hep::ReconstructedParticleData pk = inParticles[k];

           for (int l=k+1; l < n; ++l) {
            edm4hep::ReconstructedParticleData pl = inParticles[l];

             for (int m=l+1; m < n; ++m) {
            edm4hep::ReconstructedParticleData pm = inParticles[m];
          
              float charge_tot = pi.charge + pj.charge + pk.charge+ pl.charge + pm.charge;

              if ( (charge_tot == total_charge) || (conj && (charge_tot == -total_charge)) ) {
                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_5plet = {pi, pj, pk,pl,pm};
                result.push_back(a_5plet);
              }
              } //end m
              } //End l
        }  // end of the loop over k
      }  // end of the loop over j
    }  // end of the loop over i

    return result;
  }

ROOT::VecOps::RVec<float>
multiplet_charge(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& multiplets) {
  ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex> results;
  int nmultiplets = multiplets.size();
  ROOT::VecOps::RVec<float> tot_charge;
  for (int i=0; i < nmultiplets; i++) {
    float charge= 0;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = multiplets[i];
    for (int k=0;k<legs.size();k++)
      charge += legs[k].charge;
    tot_charge.push_back(charge);
  }

  return tot_charge;
}

  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>
  build_AllTauVertexObject(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& multiplets,
                           const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks) {
    ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex> results;
    int nmultiplets = multiplets.size();
    for (int i=0; i < nmultiplets; i++) {
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = multiplets[i];

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
      double mass = tau5pi_vertex_mass(v);
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
