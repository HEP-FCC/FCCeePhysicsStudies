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
  const double TAU_MASS = 1.7768;  // GeV
  const double SQRTS =91.188;  // GeV
  const int nPions=3;

 // double vertex_chi2(const edm4hep::VertexData& vertex) {
 //   return vertex.chi2;
 // }

//int vertex_ndf(const edm4hep::VertexData& vertex) {
//    return vertex.ndf;
//  }

int tauMCMode(const MCParticle tau) {
  
  /// some calcutions
  int decayModeID = 0;
  // exploration of the tau decya tree
  
  return decayModeID;
  
}

  double tau3pi_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex) {
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

  double tau3pi_vertex_energy(const VertexingUtils::FCCAnalysesVertex& vertex) {
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

    return tau.E();
  }

  double tau3pi_vertex_mom(const VertexingUtils::FCCAnalysesVertex& vertex) {
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

    return tau.Vect().Mag();
  }

  double tau3pi_vertex_cosAngle(const VertexingUtils::FCCAnalysesVertex& vertex) {
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
    edm4hep::VertexData vData = FCCAnalyses::VertexingUtils::get_VertexData(vertex);
    double rx= vData.position.x;
    double ry= vData.position.y;
    double rz= vData.position.z;
    TVector3 rvec(rx,ry,rz);
    double r =rvec.Mag();
    TVector3 mom = tau.Vect();
    double momAbs = mom.Mag();

    if (r>0 && momAbs>0)
      return  rvec.Dot(mom)/(r*momAbs);
    else
      return -999.;
  }

  double tau3pi_vertex_cosAngle(const VertexingUtils::FCCAnalysesVertex& vertex,const edm4hep::Vector3d & vtrue) {
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

    double rx= vtrue.x;
    double ry= vtrue.y;
    double rz= vtrue.z;
    TVector3 rvec(rx,ry,rz);
    double r =rvec.Mag();
    TVector3 mom = tau.Vect();
    double momAbs = mom.Mag();

    if (r>0 && momAbs>0)
      return  rvec.Dot(mom)/(r*momAbs);
    else
      return -999.;
  }

  double tau3pi_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& legs) {
    TLorentzVector tau;
    int n = legs.size();
    //cout << n << endl;
    for (int ileg=0; ileg < 3; ileg++) {
      TLorentzVector leg;
      leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, PION_MASS);
      tau += leg;
    }

    return tau.M();
  }

 double tau3pi_MC_mass(const ROOT::VecOps::RVec< int >& indices,const ROOT::VecOps::RVec<edm4hep::MCParticleData>& parts) {
   ROOT::Math::PxPyPzMVector tau;
   for (int ileg=0;ileg<3;ileg++) {
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

   ROOT::VecOps::RVec<double>
  build_neutrinoMassSquared(const ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>& vertices) {
    ROOT::VecOps::RVec<double> results;
    for (const auto& v: vertices) {
      double mH = tau3pi_vertex_mass(v);
      double eH = tau3pi_vertex_energy(v);
      double pH = tau3pi_vertex_mom(v);
      double cosAngle = tau3pi_vertex_cosAngle(v);
      double Etau = SQRTS/2;
      double ptau = sqrt(Etau*Etau-TAU_MASS*TAU_MASS);
      if(abs(cosAngle)<1 && mH>0 && eH>0 && pH>0) {
          double mnu2 =mH*mH+TAU_MASS*TAU_MASS -2*Etau*eH+2*ptau*pH*cosAngle;
         results.push_back(mnu2);
      }
    }

    return results;
  }

  double
  build_neutrinoMassSquared(const VertexingUtils::FCCAnalysesVertex & v) {
   double result = -9999.;
      double mH = tau3pi_vertex_mass(v);
      double eH = tau3pi_vertex_energy(v);
      double pH = tau3pi_vertex_mom(v);
      double cosAngle = tau3pi_vertex_cosAngle(v);
      double Etau = SQRTS/2;
      double ptau = sqrt(Etau*Etau-TAU_MASS*TAU_MASS);
      if(abs(cosAngle)<1 && mH>0 && eH>0 && pH>0) {
          result =mH*mH+TAU_MASS*TAU_MASS -2*Etau*eH+2*ptau*pH*cosAngle;
      }
    return result;
  }

  double
  build_neutrinoMassSquared(const VertexingUtils::FCCAnalysesVertex & v, const edm4hep::Vector3d & vtrue) {
   double result = -9999.;
      double mH = tau3pi_vertex_mass(v);
      double eH = tau3pi_vertex_energy(v);
      double pH = tau3pi_vertex_mom(v);
      double cosAngle = tau3pi_vertex_cosAngle(v,vtrue);
      double Etau = SQRTS/2;
      double ptau = sqrt(Etau*Etau-TAU_MASS*TAU_MASS);
      if(abs(cosAngle)<1 && mH>0 && eH>0 && pH>0) {
          result =mH*mH+TAU_MASS*TAU_MASS -2*Etau*eH+2*ptau*pH*cosAngle;
      }
    return result;
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
