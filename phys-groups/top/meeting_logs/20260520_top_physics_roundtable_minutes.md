# FCC Top Physics Group — First Roundtable Meeting

**Date:** 20 May 2026 · **Time:** 14:05–15:54

**Chairs:** Xunwu Zuo, Gauthier Durieux, Jürgen Reuter, Christian Schwanenberger

**Attending (speaking):** Xunwu Zuo, Gauthier Durieux, Jürgen Reuter, Christian Schwanenberger, Jacopo De Piccoli, Lukas Allwicher, Michele Selvaggi, David D'Enterria, Daniel Reichelt

## Contributions

### Jürgen Reuter — Generators for the top threshold

**Main conclusions**
- NRQCD threshold calculation (N³LO + velocity resummation) implemented in Whizard via a Green's-function effective coupling, matched to relativistic NLO through a velocity-dependent switch-off function.
- Differential threshold-resummed results available at NLL accuracy; QED ISR included at NLL.
- To push theory error below ~20 MeV an N⁴LO calculation is needed.
- Still to be done: differential treatment away from the top pole, NNLL matching, and the soft-gluon / parton-shower interface.

**Discussion**
- Schwanenberger asked how the matching between NRQCD and relativistic NLO is performed; Reuter explained the expansion in αs, subtraction to avoid double counting, and the velocity-dependent switch-off function (included in the theory error band).
- Selvaggi: for the fully inclusive threshold scan a reweighted Beneke et al. calculation likely suffices; a more accurate differential MC matters mainly for acceptance systematics and for kinematic / template-based exploitation of the decay.
- The threshold MC uses a short-distance top mass, avoiding the usual MC-mass ambiguity — modulo soft-gluon matching to the parton shower, which remains to be studied.

### Jacopo De Piccoli — SMEFT fit at the tt̄ threshold with FCC-ee

**Main conclusions**
- 12 EFT operators (neutral-coupling and e⁺e⁻–tt̄ contact types) studied via per-event reweighting of Whizard tt̄ semileptonic samples (Delphes/IDEA) using MadGraph weights.
- Matrix-element-based optimal discriminators (Neyman–Pearson) combined into an n-dimensional observable with 2 bins per dimension.
- Adding sub-threshold points (340, 345 GeV) lifts degeneracies present at a single centre-of-mass energy.
- Sub-threshold runs add real constraining power even on top of HL-LHC projections.
- Paper planned soon; covariance-matrix checks are the main remaining step.

**Discussion**
- Reuter / Selvaggi: the assumed luminosity distribution across the scan may not be optimal for a global EFT fit and should be revisited — the current allocation (~400 fb⁻¹ below threshold, 3 ab⁻¹ above) is already overkill for the top-mass statistical reach.
- Zuo asked about the reweighting workflow: weights extracted from MadGraph tt̄ and applied to Whizard WBWB samples — suboptimal (single-top contributions not reweighted optimally) but validated against direct generation.
- Reuter asked whether spin correlations could help lift flat directions; Durieux / Selvaggi: spin information is already fully exploited because the discriminants are matrix-element-based.
- Durieux noted that optimality of the matrix-element observable was proven analytically at the linear, stat-only level (Diehl / Nachtmann, early 1990s).

### Lukas Allwicher — Electron–top operators and the Higgs trilinear at FCC-ee

**Main conclusions**
- With only κ₃ floating, FCC-ee reaches ~17% precision on the Higgs trilinear via e⁺e⁻→ZH loop contributions (sensitivity scale ~1 TeV).
- Five eett operators enter ZH at the same perturbative order and can spoil κ₃ if left unconstrained — current EWPOs alone degrade κ₃ to ~30%.
- Combining EWPOs, Drell–Yan, RB/RC, RT and ZH at FCC-ee lifts all flat directions in the eett subspace and recovers the κ₃-only sensitivity.
- Conclusion: electron–top interactions do not jeopardise the Higgs trilinear extraction.

**Discussion**
- Durieux: the analysis includes only eett operators and excludes Z–top coupling modifications, which are degenerate with vector eett currents at a single √s.
- Specifically, the orthogonal combination of left-handed singlet and triplet operators is constrained only via Z→bb̄ at tree level; the residual flat direction may still affect the global fit. Allwicher agreed this is worth checking explicitly.
- Z→bb̄ at multiple energies (WW, ZH, tt̄) provides useful additional handles.

### Xunwu Zuo — Direct |Vts| from top decays at FCC-ee

**Main conclusions**
- Existing |Vts| determinations are limited: Bs mixing reaches ~2.2% but is theory-dominated and SM-only; LHC single-top constraints are ~100% and degenerate with |Vtd|.
- At FCC-ee with 2 M tt̄ events, ~6,000 t→Ws decays give a projected ~3.1% statistical precision on |Vts| — comparable to the best current determination and theory-independent.
- The analysis is essentially complete for |Vts| (FCC note + GitHub code); plan is to extend to |Vtb| in common effort with the electroweak WW CKM analysis.
- |Vts| precision improved from ~7–8% to 3.1% just from a better tagger version — further tagger gains can move the result.

**Discussion**
- D'Enterria asked why the precision is 3.1% rather than the naive 1.2% on 6,600 events; Zuo explained acceptance loss and irreducible background contribute, and the analysis already relies on ~10⁻³ b-jet fake rate.
- Selvaggi: an obvious next step is to retrain the jet flavour tagger on tt̄ at 365 GeV (current tagger trained on Z→qq̄ at the Z pole — different topology).
- Schwanenberger / D'Enterria: a semi-direct |Vtd| extraction by veto + multi-class tagging (b vs s vs ud) is worth pursuing — would be the first direct constraint on |Vtd|. D'Enterria offered to set this up with students.
- Reuter: jet charge from the semileptonic side helps fix top/anti-top assignment, reducing the need to separate up from down in the light-jet tagger.


