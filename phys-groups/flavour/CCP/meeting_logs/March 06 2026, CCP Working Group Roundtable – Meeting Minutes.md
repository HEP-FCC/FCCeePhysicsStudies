
# March 06 2026, CCP Working Group Roundtable – Meeting Minutes

**Date/Time:** ~16:02 (from transcript)  
**Chair:** Xunwu Zuo  

## Participants (speaking)
- Xunwu Zuo  
- Andreas Jüttner  
- Christoph Schwanda  
- Stephane Monteil  
- Vasilisa Guliaeva  
- Christina Agapopoulou  
- Zoltan Ligeti  
- Additional participants

---



# Presentation Summaries

## 1 Lattice QCD Requirements (Andreas Jüttner)

### Objective

Define **precision requirements for lattice QCD calculations** that support FCC flavor physics analyses.

### Key Points

- Compile theoretical quantities requiring improved precision over the next **10–20 years**
- Build on previous work from the **Flavor Lattice Averaging Group (FLAG)**

### The Vcb Puzzle

A persistent discrepancy exists between:

- **Inclusive Vcb measurements**
- **Exclusive Vcb measurements**

Error analysis shows uncertainties are largely dominated by:

- Lattice form factor calculations
- Branching fraction measurements

### Discussion

Current experimental limitations at B factories include:

- Minimum lepton energy thresholds
- Difficult to simulate slow pions in D* decays

Potential improvements at **FCC-ee (Z pole)**:

- Boosted B mesons allow full phase-space coverage
- Slow pion reconstruction becomes easier

---

## 2 Purely Leptonic B Decays at FCC (Vasilisa Guliaeva)

### Physics Motivation

Purely leptonic decays such as **B → τν** and **B → μν**:

- Provide **clean determinations of CKM parameters**
- Offer sensitive tests of **lepton flavor universality**
- Provide potential signals of **new physics**

### Analysis Strategy

Signal events typically contain:

- One visible lepton
- Large missing energy due to neutrinos

Methodology:

1. Divide events into hemispheres using the **thrust axis**
2. Apply initial selection cuts
3. Use **BDT classification (XGBoost)** for signal-background separation


### Preliminary Results

- ~20% signal efficiency for τ channels
- Strong suppression of backgrounds


### Future Work

Planned developments include:

- Studying additional τ decay channels
- Investigating **radiative decays (B → μνγ)**
- Applying **transformer-based particle networks**
- Improving modeling of hadronization fractions

### Discussion Highlights

Participants discussed:

- Detector performance assumptions
- Fast simulation vs full detector simulation
- Charm hadron background Ds -> tau, 
- Z->cc, Z->bbcc backgrounds
- Potential inclusive Bc hadron tagger for production fraction

---

## 3 Direct Vts Measurement via Top Decays (Xunwu Zuo)

### Motivation

Current **Vts measurements** are obtained from **Bs–Bs̄ mixing**, which depends heavily on lattice QCD inputs.

A direct measurement via **t → Ws decay** would provide a more **model-independent determination**.

### FCC-ee Prospects

Expected signal statistics:

- ~6000 **t → Ws events**

Estimated precision:

- ~3% for **Vts**
- Potential **per‑mille precision** for **Vtb**

### Key Challenge

The measurement precision strongly depends on **jet flavor tagging calibration**.

### Future Plans

- Extend the analysis to measure **Vtb**
- Improve evaluation of tagging uncertainties
- Seek additional collaborators for the study

---

# Open Discussion / Brainstorming

Participants discussed priorities for the working group.

### Key Points

- Determining **Vcb at the W threshold** was highlighted as a **major priority**
- This measurement is important for:
  - understanding the **Vcb anomaly**
  - calibrating **jet flavor tagging** for the FCC program

Additional suggested activities:

- Further work on **semileptonic B decays**
- Development of **inclusive flavor tagging tools**
- Coordination with external groups studying **Bc hadronization fractions**

---


# Silent Contributions

## CKM Measurements from On-Shell W Decays (Michele Tammaro)

CKM elements can be extracted from hadronic W decays.

Precision is expected to depend strongly on flavour tagging performance.

No plan for further work but happy to provide info for other interested people

---

## FEI Reconstruction Tools (Valerio Bertacchi)

Full Event Interpretation reconstructs complete B decay chains using machine-learning-based hierarchical reconstruction.

Potential FCC-ee developments include graph neural networks and transformer-based algorithms.

---

## Rare Decays: b → sℓ⁺ℓ⁻ (Riccardo Silva Coutinho)

Study of rare B decays probing flavour anomalies.

A “sum-of-exclusive” analysis reconstructs multiple exclusive channels to approximate inclusive observables.

The method uses a DFEI-inspired deep-learning approach with graph neural networks.

FCC-ee could significantly improve precision in these measurements.

---

## Semileptonic B Decay Studies (Matthew Rudolph)

Interest expressed in semileptonic B decays and the application of DFEI algorithms to inclusive and tagging studies.

Possible student involvement starting summer 2026.

---

## Heavy Quark Symmetry Sum Rules (Syuhei Iguro)

Heavy-quark symmetry allows predictive relations among semileptonic decays.

Example relation connects LFU ratios for Λc, D, and D* channels and can help test anomalies.

---

# End of Minutes
