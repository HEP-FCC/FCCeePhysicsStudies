# Charge Current Process Working Meeting — Minutes

## Attendees

- Xunwu Zuo
- Vasilisa Guliaeva
- Lesya Shchutska
- Stephane Monteil
- Guy Wilkinson
- Markus Prim
- Zoltan Ligeti
- Matthew S. Rudolph
- Keisho Hidaka

## General Items

1. **Poster submissions for FCC Week**  
   Participants are encouraged to submit posters for FCC Week. Anyone submitting a poster should inform the organizers so they can keep track.

2. **FCC Flavour Workshop in June**  
   The group discussed planning for the FCC Flavour Workshop session in June. The CCP group can prepare a proposed agenda and speaker list, then share it with Stephane Monteil and Guy Wilkinson for coordination and consistency checks.

3. **Next CCP working meeting**  
   The next CCP working meeting may be scheduled toward the end of May or beginning of June, depending on available contributions.


## Contribution: hadron tagger

### Presentation Summary

Xunwu Zuo presented progress on a hadron-flavour tagger based on a Particle Transformer architecture. The tagger is intended to identify hadron species such as $B_c$, $B_s$, $B_u/B_d$, and $\Lambda_b$ for inclusive $B$-decay studies, hadronization-fraction measurements, and signal selection.

The study compared several training configurations, including one-hemisphere versus full-event inputs, and cases where signal-decay products and/or neutral particles were removed. The tagger performs well overall, especially for $B_c$ tagging. The hardest separation is $B_d$ versus $B_s$. The opposite hemisphere provides only a modest improvement, while much of the tagging power comes from the signal decay itself.

Vasilisa Guliaeva summarized a calibration strategy using fully reconstructible exclusive $B_c$ decay chains. The plan is to classify decay topologies, measure per-decay tagger efficiencies, propagate branching-ratio uncertainties, and combine these into an uncertainty on inclusive tagging efficiency.

### Main Points from Discussion

- **Hadronization modelling**: The group noted that the tagger performance depends on how hadronization is modelled in Monte Carlo, particularly in Pythia. Comparing with other generators or generator settings, such as Herwig, was suggested as a way to assess model dependence.

- **Hemisphere correlation and low-energy tracks**: The modest improvement from using the opposite hemisphere may come from residual correlations between hemispheres. It was suggested to test this by removing low-energy tracks, since soft particles may carry more of the colour-connection or hadronization-related correlation.

- **Modelling of multi-heavy-flavour decays**: The discussion raised concerns about whether the simulation correctly models events with multiple heavy-flavour pairs, such as additional charm production. The team should check what is included in the current Pythia setup and whether existing LEP, LHC, or B-factory measurements can help validate the modelling.

- **Tag-and-probe alternative**: An alternative calibration strategy based on single-tag and double-tag equations was discussed. Using known hadronization fractions could allow some efficiencies or additional fractions to be constrained directly from data, though the details require further offline work.