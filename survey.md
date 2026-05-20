# Multijet Background Modelling at the LHC: A Practical Survey

Prepared for Zhi Zheng  
Date: 20 May 2026

## Executive summary

Multijet background modelling is one of the central experimental problems in hadron-collider analyses. The core difficulty is not that QCD multijet production is conceptually unknown, but that the regions relevant for many searches and Higgs measurements are rare, highly selected tails: jets misidentified as heavy-flavour jets, jets faking leptons or photons, ordinary QCD events acquiring large apparent missing transverse momentum, or smooth QCD continuum events entering a narrow mass window. These tails are sensitive to flavour composition, detector response, trigger biases, jet energy calibration, tagging algorithms, and correlations introduced by multivariate classifiers. For this reason, ATLAS and CMS rarely rely on pure QCD simulation for the final multijet estimate.

Across LHC analyses, the most common solutions fall into a few broad families:

1. **Smooth analytic fits to data**: fit the mass spectrum with flexible empirical functions and search for a localized signal bump.
2. **Sideband / transfer-factor methods**: use a signal-depleted data region and extrapolate into the signal region.
3. **Pass/fail or tag-rate methods**: use events failing a tag requirement to predict events passing it.
4. **Loose/tight fake-factor and matrix methods**: estimate fake-object backgrounds from relaxed object selections.
5. **ABCD methods**: use two approximately independent variables to infer the background in the signal region from three control regions.
6. **Template methods with decorrelated classifiers**: design the classifier so it does not sculpt the final discriminant, allowing a control region to constrain the signal region shape.
7. **Rebalance-and-smear methods**: model fake missing-transverse-momentum tails by rebalancing low-MET data and smearing jets by detector response functions.
8. **ML-assisted generative or reweighting approaches**: increasingly explored, but still limited by validation and systematic-uncertainty assignment.

The three papers discussed in the conversation illustrate three different points in this landscape:

- **CMS VBF H(bb), arXiv:2308.01253**: QCD multijet is treated as a smooth continuum in the b-jet-pair invariant mass, modelled directly in data using an exponential times polynomial function in each category. The function order is selected using sidebands and an F-test; bias is checked with pseudo-data from alternative functions.
- **ATLAS VBF H(bb), arXiv:2011.08280**: an adversarial neural network is trained to classify VBF-like events while being decorrelated from the bb invariant mass. This allows the non-resonant multijet mass shape to be shared across ANN-score regions within a channel and constrained primarily by the low-score, high-statistics region. Residual shape bias is evaluated in dedicated control regions.
- **HWW entanglement paper, arXiv:2605.19754**: this is not mainly a multijet-background paper. It uses MC templates for WW, ttbar, and Z→ττ with normalization and unfolding-shape nuisance parameters. It is useful as an example of profile-likelihood template fitting, but its background treatment is not a full data-driven multijet estimate.

A useful way to summarize the field is: **if the background is smooth under a narrow signal peak, fit it from data; if the background enters through fake objects, measure fake rates in data; if the background is defined by a tagger, use pass/fail or tag-rate transfer factors; if a classifier is used, decorrelate it from the final mass variable or validate the induced sculpting; if fake MET is the issue, model detector response directly.**

---

## 1. Why multijet backgrounds are difficult

QCD multijet production has an enormous cross section at the LHC. In many analyses the multijet contribution becomes dangerous only after a combination of rare effects:

- light- or charm-flavour jets are misidentified as b jets;
- jets fake isolated leptons, photons, or hadronic τ candidates;
- heavy-flavour decays produce non-prompt leptons;
- jet energy mismeasurement creates large apparent missing transverse momentum;
- boosted-object taggers select rare two-prong or heavy-flavour-like QCD jets;
- multivariate classifiers sculpt mass distributions;
- trigger and offline thresholds bias the reconstructed mass or jet-pairing distribution.

The final selected sample often lives in a small and detector-sensitive corner of QCD phase space. A fully simulated multijet sample may be useful for optimization or closure tests, but it is usually not trusted for the final rate and often not for the final shape.

Two modelling questions should always be separated:

- **Normalization**: how many multijet events enter the signal region?
- **Shape**: what is their distribution in the final discriminating observable?

Some methods estimate both from data. Others take shape from a control region and normalization from a fit. The strongest analyses usually use several control and validation regions and include the background constraints directly in a simultaneous likelihood fit.

---

## 2. Case study I: CMS VBF H→bb, arXiv:2308.01253

### 2.1 Physics context

The analysis measures vector-boson-fusion Higgs production with H→bb using 13 TeV CMS data. The final state has two b-tagged jets from the Higgs candidate and two additional jets forming the VBF topology. The main observable for signal extraction is the invariant mass of the selected b-jet pair, \(m_{bb}\).

The dominant background is QCD multijet production, producing a smooth non-resonant continuum in \(m_{bb}\). A resonant Z+jets background, especially Z→bb, produces a peak around the Z mass and must be modelled separately.

### 2.2 Multijet model

CMS models the QCD continuum in each event category with an analytic function fit directly to data:

\[
F_i^{\mathrm{QCD}}(m_{bb}) = \exp(-b_i m_{bb})\left(1 + \sum_{j=1}^{n} a_{ij} m_{bb}^{j}\right),
\]

where \(i\) labels the category. The normalization and the shape parameters are extracted from the fit. This is a standard resonance-search strategy: the signal is a localized peak near 125 GeV, while QCD is assumed to be smooth over the fitted mass range.

### 2.3 Choosing the function

The function order is chosen using sidebands, avoiding the Higgs mass region. CMS uses the sideband ranges

- \(80 < m_{bb} < 104\) GeV,
- \(146 < m_{bb} < 200\) GeV.

Sequential fits with increasing polynomial order are performed, and a Fisher F-test selects the minimal function complexity needed to describe the data. This is meant to avoid both underfitting, which could fake a signal, and overfitting, which could absorb a real signal.

### 2.4 Resonant Z+jets component

Z+jets is not treated as part of the smooth QCD continuum. CMS models the resonant Z→bb contribution with parametric shapes derived from simulation: a one-sided Crystal Ball function for the resonant peak plus a second-order Bernstein polynomial for wrong jet pairings and non-peak contributions. Dedicated Z-enriched categories constrain the Z+jets normalization, which is then propagated to other categories.

### 2.5 Bias studies

CMS tests whether the chosen QCD function can bias signal extraction. Alternative continuum models are used to generate pseudo-data, including:

- functions from the same exponential-polynomial family but with higher polynomial order;
- inverse polynomials.

The nominal model is then used to fit the pseudo-data, and the extracted signal is compared with the injected signal. The maximum potential bias is reported to be below 10% of the statistical uncertainty on the fitted signal rate in each individual category, making the function-choice uncertainty subdominant.

### 2.6 Strengths and limitations

**Strengths**

- Directly data-driven for the dominant QCD component.
- Transparent and familiar bump-hunt strategy.
- Flexible per-category modelling.
- Function-choice bias is explicitly tested.

**Limitations**

- Relies on QCD smoothness in \(m_{bb}\).
- Depends on the choice of empirical function and sideband definition.
- High-purity categories can have limited sideband statistics.
- If a BDT or category selection sculpts \(m_{bb}\), a simple smooth function can become risky.
- It does not share much shape information across categories.

---

## 3. Case study II: ATLAS VBF H→bb, arXiv:2011.08280

### 3.1 Physics context

This ATLAS measurement also targets VBF H→bb in a four-jet topology. The main observable is again \(m_{bb}\). The dominant background is non-resonant QCD multijet production; Z→bb is a resonant background.

The methodological novelty is the use of an adversarial neural network (ANN) to classify VBF-like events while suppressing correlations between the classifier score and \(m_{bb}\).

### 3.2 Why mass decorrelation matters

A powerful classifier can easily learn variables correlated with \(m_{bb}\). If the classifier output is correlated with the final mass variable, selecting high-score events sculpts the background mass spectrum. This can make a smooth QCD background look different in high- and low-score regions, or even produce artificial local structures near the signal window.

ATLAS addresses this by using an adversarial setup:

- the classifier tries to distinguish signal-like from background-like events;
- the adversary tries to infer the \(m_{bb}\) bin from the classifier output;
- the classifier is penalized if the adversary can predict \(m_{bb}\).

The goal is to make the classifier score approximately independent of \(m_{bb}\) for the background.

### 3.3 Training sample

The signal training sample comes from VBF H→bb simulation. The background sample comes from data sidebands rather than multijet simulation, because the multijet MC does not fully capture the data complexity. The sidebands are roughly

- \(70 < m_{bb} < 100\) GeV,
- \(140 < m_{bb} < 200\) GeV.

Multi-jet simulation is used for architecture and performance studies, but data sidebands are used for the final discriminant training.

### 3.4 Non-resonant background shape model

The non-resonant QCD background shape is a binned distribution in \(m_{bb}\), shared across ANN-score regions within each channel. Its normalization is allowed to float independently in each region. Symbolically,

\[
Y_{ijk} = \mu N^H_{ijk} H_{ijk} + N^B_{ij} B_{ik} + \mu_Z N^Z_{ijk} Z_{ik} + \cdots,
\]

where \(i\) labels the channel, \(j\) the ANN-score region, and \(k\) the \(m_{bb}\) bin. The key point is that \(B_{ik}\) has no region index \(j\): the shape is shared among regions. The low-score region, which contains much more data, primarily constrains this common background shape.

This method trades functional-form uncertainty for a decorrelation assumption: if the ANN score is independent of \(m_{bb}\), then the shape can be shared across regions.

### 3.5 Resonant Z→bb background

ATLAS estimates the Z→bb resonant background using a Z→μμ embedding method. Z→μμ data events are selected, the muons are replaced with simulated b-quark showers with matching four-vectors, and the modified events are passed through reconstruction, selection, and categorization. This provides a data-driven handle on the event environment while modelling the b-jet showering with simulation. A 20% non-closure uncertainty is assigned based on validation studies.

### 3.6 Shape-bias control regions

The main risk is that the shared-shape assumption is not exact. ATLAS evaluates this with dedicated shape-bias control regions. These are built by inverting or modifying selections to produce orthogonal samples with similar kinematics. The control-region events are translated and reweighted to better match signal-region kinematics, then passed through the ANN.

The procedure tests whether using a common non-resonant shape can generate a fake Higgs-like signal. A bias signal with the Higgs-like shape is scanned over mass values from 100 to 140 GeV, and the largest observed fake signal is taken as an additional uncertainty. The bias uncertainty ranges from large fractions of the expected signal in less sensitive regions to smaller values in the most sensitive regions.

### 3.7 Strengths and limitations

**Strengths**

- Uses data sidebands rather than relying on QCD MC.
- Avoids specifying an empirical analytic function for the QCD shape.
- Uses low-score, high-statistics regions to constrain high-score regions.
- Explicitly addresses mass sculpting by the classifier.
- Well suited to multivariate categorization.

**Limitations**

- Relies on successful decorrelation between classifier score and \(m_{bb}\).
- More complex and less transparent than an analytic fit.
- Sideband training cannot directly validate the Higgs mass window.
- The shared-shape assumption needs substantial control-region validation.
- Decorrelation can reduce classifier power if the most discriminating variables are correlated with the mass.

---

## 4. Case study III: HWW entanglement, arXiv:2605.19754

This paper is useful for comparison because it uses a profile-likelihood template strategy, but it is not primarily a multijet-background modelling paper.

The signal process is H→WW*→ℓνℓν. The dominant backgrounds considered are non-resonant WW, ttbar, and Z→ττ. The analysis constructs a continuous CGLMP-inspired observable \(I_3\) and performs a template-shape hypothesis test between entangled and separable signal hypotheses.

The background model is based on MC templates with nuisance parameters:

- WW normalization uncertainty: 20%,
- ttbar normalization uncertainty: 10%,
- Z→ττ normalization uncertainty: 15%,
- additional shape uncertainties from cDDPM unfolding closure residuals.

This is a useful example of HistFactory/RooFit-style simultaneous template fitting, but it is not a complete data-driven background estimate. A full experimental HWW analysis would also need data-driven control regions for WW, ttbar, Z→ττ, and fake/non-prompt lepton backgrounds. In particular, fake-lepton or multijet backgrounds would usually require fake-factor, matrix-method, or same-sign control-region techniques.

---

## 5. Broader taxonomy of multijet background methods

### 5.1 Smooth analytic fits

**Basic idea**: if the signal is a localized mass peak and the background is smooth, model the background with an analytic function fitted to data.

Common functions include exponentials times polynomials, Bernstein polynomials, power-law forms, inverse polynomials, or families of empirical resonance-search functions.

**Advantages**

- Very transparent.
- Does not require QCD MC normalization.
- Naturally fits bump searches.
- Bias can be studied with pseudo-data from alternative functions.

**Limitations**

- Function choice is empirical.
- Classifier-induced mass sculpting can violate smoothness assumptions.
- Overfitting can absorb signal; underfitting can fake signal.
- Sideband statistics can limit the method.

**Representative examples**

- CMS VBF H→bb, arXiv:2308.01253.
- Many dijet, diphoton, and resonance searches.

### 5.2 Sideband and transfer-factor methods

**Basic idea**: define a signal-depleted region close to the signal region and extrapolate with a transfer factor:

\[
N_{\mathrm{SR}}^{\mathrm{QCD}} = T \times N_{\mathrm{CR}}^{\mathrm{data}}.
\]

The transfer factor may come from simulation, data sidebands, tag-rate measurements, or a simultaneous fit.

**Advantages**

- Data-driven normalization.
- Flexible and broadly applicable.
- Fits naturally into simultaneous likelihood models.

**Limitations**

- Transfer factors depend on kinematics and object composition.
- Signal contamination in the control region must be controlled.
- Closure tests are essential.
- Shape extrapolation can be more difficult than yield extrapolation.

### 5.3 Pass/fail and tag-rate methods

**Basic idea**: use a tagger to define pass and fail regions. The fail region is background-rich; the pass region is signal-enriched. A pass-to-fail ratio predicts QCD in the pass region from the fail region:

\[
N_{\mathrm{pass}}^{\mathrm{QCD}}(x) = R_{p/f}(x)\,N_{\mathrm{fail}}^{\mathrm{QCD}}(x),
\]

where \(x\) can include jet mass, jet \(p_T\), substructure variables, or category labels.

**Advantages**

- Very natural for boosted H→bb, diboson, top-tag, and b-tag analyses.
- Uses data in the fail region to constrain QCD shape.
- Can be implemented in a simultaneous pass/fail fit.

**Limitations**

- The pass/fail ratio can depend on many variables.
- Taggers can sculpt jet mass distributions.
- Requires careful decorrelation or transfer-factor parameterization.
- High-purity pass regions may have limited data.

**Representative examples**

- CMS inclusive boosted H→bb, arXiv:1709.05543, where boosted H→bb is reconstructed as a single large-radius jet and QCD is controlled through tag-related categories.
- Modern boosted HH→bbbb and boosted resonance searches often use variants of pass/fail background modelling.

### 5.4 ABCD method

**Basic idea**: choose two approximately independent variables and define four regions. If the variables are independent for the background,

\[
N_A \approx \frac{N_B N_C}{N_D},
\]

where A is the signal region and B, C, D are control regions. A correction factor \(\kappa\) is often used:

\[
N_A = \kappa \frac{N_B N_C}{N_D}.
\]

**Advantages**

- Simple and highly data-driven.
- Useful for fake-object and QCD estimates.
- Easy to explain.

**Limitations**

- Independence is rarely exact.
- Correlations become a major systematic.
- Shape estimation requires additional assumptions.
- Signal contamination in sidebands must be treated.

### 5.5 Matrix method and fake-factor method

These are most relevant when multijet enters through fake or non-prompt leptons, photons, or τ candidates.

**Matrix method**: define loose and tight object selections. Measure the probability for real and fake loose objects to pass tight criteria, then solve for the fake contribution in the tight region.

**Fake-factor method**: define an anti-tight or fail-ID region and multiply by a fake factor measured in a fake-enriched control region.

**Advantages**

- Standard tools for fake-lepton and fake-τ backgrounds.
- Mostly data-driven.
- Can estimate both yield and shape using anti-ID data.

**Limitations**

- Fake rates depend on \(p_T\), \(\eta\), flavour, jet multiplicity, b-tag multiplicity, and event topology.
- Prompt contamination must be subtracted.
- Control-region fake composition may not match the signal region.
- Shape uncertainties are often large.

### 5.6 Same-sign methods

**Basic idea**: use same-sign lepton or τ pairs as a fake-enriched control region and extrapolate to opposite-sign signal regions using an OS/SS ratio.

**Advantages**

- Simple and data-driven.
- Useful for dilepton or τ analyses.
- Signal contamination is often small in the same-sign region.

**Limitations**

- OS/SS ratio may depend on heavy-flavour composition, charge misidentification, and kinematics.
- Prompt same-sign backgrounds must be subtracted.
- Shape transfer must be validated.

### 5.7 Rebalance and smear

**Basic idea**: model QCD fake-MET tails using data. First rebalance jets in low-MET events to estimate the underlying hard-scatter kinematics, then smear the jets with detector response functions to predict the high-MET tail.

**Advantages**

- Directly targets jet-mismeasurement fake MET.
- Uses real multijet data.
- Powerful for all-hadronic SUSY and jets+MET searches.

**Limitations**

- Requires accurate jet response functions, including non-Gaussian tails.
- Complex implementation.
- Less applicable to fake-lepton or mass-bump backgrounds.

**Representative example**

- CMS searches for supersymmetry in multijet + missing-transverse-momentum final states use rebalance-and-smear-style QCD estimates.

### 5.8 Data-template reweighting for heavy-flavour multijet final states

**Basic idea**: use a lower-tag or control sample, such as a 2-tag sample, to predict a higher-tag signal region, such as a 4-tag sample. Apply combinatorial and kinematic reweighting from sidebands.

**Advantages**

- Very useful for HH→bbbb and multi-b final states.
- Avoids reliance on simulated heavy-flavour multijet rates.
- Captures much of the real detector and flavour-tagging environment.

**Limitations**

- Transfer from low-tag to high-tag regions can depend strongly on flavour composition.
- Reweighting variables must be chosen carefully.
- Closure and validation regions are essential.

**Representative example**

- ATLAS HH→bbbb searches, e.g. arXiv:1804.06174, use lower-b-tag data samples reweighted to model multijet backgrounds in high-b-tag signal regions.

### 5.9 ML-assisted background modelling

**Basic idea**: use machine learning to decorrelate classifiers, reweight control regions, interpolate sidebands, or model high-dimensional background distributions.

Examples include adversarial decorrelation, CWoLa-style weak supervision, normalizing flows, diffusion models, and neural simulation-based inference.

**Advantages**

- Can handle high-dimensional correlations.
- May improve transfer factors or background templates.
- Natural for complex boosted or multi-object final states.

**Limitations**

- Validation and systematic-uncertainty assignment are difficult.
- Signal contamination can bias training.
- Extrapolation outside the training support is dangerous.
- Interpretability is weaker than analytic fits or simple sideband methods.

The ATLAS VBF H→bb adversarial-network analysis is a good example of ML used conservatively: not to generate the background, but to enforce a property, mass decorrelation, that makes a data-driven background model more reliable.

---

## 6. Comparison table

| Method | Basic idea | Best suited for | Strengths | Main limitations |
|---|---|---|---|---|
| Smooth analytic fit | Fit a smooth mass spectrum directly in data | Bump hunts, H→bb, dijet/diphoton searches | Transparent, data-driven, standard | Function choice, mass sculpting, sideband statistics |
| Shared template + decorrelated classifier | Make classifier independent of final mass, share QCD shape across regions | MVA-based bump hunts | Uses high-stat control regions, avoids arbitrary function | Decorrelating classifier is hard; shared-shape assumption needs validation |
| Sideband / transfer factor | Extrapolate from signal-depleted data to signal region | Many searches | Flexible and data-driven | Transfer-factor closure and signal contamination |
| Pass/fail / tag-rate | Predict tagged region from untagged or fail-tag data | Boosted objects, b-tag, τ-tag, photon fake | Natural for tagger analyses | Tagger-mass correlations, high-dimensional dependence |
| ABCD | Infer SR from three CRs using two uncorrelated variables | QCD/fake backgrounds | Simple, robust if independent | Variable correlations dominate uncertainty |
| Matrix method | Solve loose/tight real/fake equations | Fake leptons | Standard and data-driven | Fake-rate dependence and composition mismatch |
| Fake-factor method | Apply tight/anti-tight ratio to fail-ID events | Fake τ, fake lepton, fake photon | Shape can come from data | Anti-ID to ID transfer uncertainty |
| Same-sign method | Use SS data to predict OS fake background | Dilepton/τ fake estimates | Simple fake-enriched CR | OS/SS ratio systematics |
| Rebalance and smear | Rebalance low-MET data and smear jets | QCD fake MET | Targets detector response tails | Complex; response tails critical |
| Low-tag to high-tag reweighting | Reweight 2-tag data to model 4-tag data | HH→bbbb, multi-b | Uses real multijet data | Flavour-composition transfer |
| ML generative/reweighting | Learn high-dimensional transfer or background density | Complex final states | Powerful correlations | Trust, validation, systematics |

---

## 7. Practical checklist for reading a paper

When evaluating a multijet background model, ask:

1. **What is the mechanism by which multijet enters?** Fake b-tags, fake leptons, fake MET, boosted-tag mistags, or a smooth continuum?
2. **Which part is taken from data?** Shape, normalization, transfer factor, fake rate, or all of them?
3. **What is the final discriminant?** Mass, BDT score, MET, transverse mass, or a multidimensional fit?
4. **Can the event selection or classifier sculpt the final discriminant?** If yes, is there decorrelation or a bias study?
5. **Are sidebands close enough to the signal region?** What variables differ, and how are they reweighted?
6. **How is signal contamination in control regions handled?**
7. **What closure tests are performed?** Alternative functions, pseudo-data, validation regions, or control-region fake-signal scans?
8. **Are normalization and shape uncertainties separated?**
9. **Are nuisance parameters included in a simultaneous likelihood fit?**
10. **Is QCD MC used only for validation, or does it drive the result?** If it drives the result, the analysis needs especially strong justification.

---

## 8. Main lessons from the surveyed papers

1. **QCD multijet is usually estimated from data, not from absolute simulation.** Simulation is useful for optimization, cross-checks, and sometimes transfer factors, but rarely for the final rate.

2. **The final discriminant determines the right method.** Mass-bump searches often use analytic fits or mass-decorrelated templates. Fake-object analyses use loose/tight fake-rate methods. MET-tail searches use response-based methods.

3. **Classifier sculpting is a central issue.** If a BDT or NN is used to define categories, the analysis must prove that it does not create artificial structures in the variable used for signal extraction. ATLAS arXiv:2011.08280 is a clean example of using adversarial decorrelation for this purpose.

4. **Control-region closure is more important than method elegance.** A simple ABCD method with excellent closure can be more reliable than a sophisticated ML method with weak validation.

5. **The best analyses separate resonant and non-resonant backgrounds.** In H→bb, Z→bb is not part of the smooth QCD continuum and usually receives a dedicated model or constraint.

6. **Bias studies are essential.** CMS uses alternative functions and pseudo-data; ATLAS uses shape-bias control regions and fake-signal scans. Both are trying to answer the same question: could the background model create or hide a Higgs-like bump?

---

## 9. References and suggested reading

### Core papers discussed

1. CMS Collaboration, “Measurement of the Higgs boson production via vector boson fusion and its decay into bottom quarks in proton-proton collisions at √s = 13 TeV,” arXiv:2308.01253, JHEP 01 (2024) 173.
2. ATLAS Collaboration, “Measurements of Higgs bosons decaying to bottom quarks from vector boson fusion production with the ATLAS experiment at √s = 13 TeV,” arXiv:2011.08280, Eur. Phys. J. C 81 (2021) 537.
3. V. Croft et al., “Hypothesis Tests for Observing Quantum Entanglement in H→WW* at the LHC,” arXiv:2605.19754.

### Additional representative analyses and method examples

4. CMS Collaboration, “Inclusive search for a highly boosted Higgs boson decaying to a bottom quark-antiquark pair,” arXiv:1709.05543, Phys. Rev. Lett. 120 (2018) 071802.
5. ATLAS Collaboration, “Search for pair production of Higgs bosons in the bbbb final state in proton-proton collisions at √s = 13 TeV with the ATLAS detector,” arXiv:1804.06174.
6. CMS Collaboration, “Search for low mass vector resonances decaying into quark-antiquark pairs in proton-proton collisions at √s = 13 TeV,” arXiv:1710.00159, JHEP 01 (2018) 097. Useful for smooth jet-mass background fitting and boosted-resonance context.
7. CMS Collaboration, “Search for supersymmetry in multijet events with missing transverse momentum in proton-proton collisions at 13 TeV,” Phys. Rev. D 96 (2017) 032003. Representative of rebalance-and-smear-style QCD fake-MET estimation.
8. CMS Open Data Guide, “Background modelling” and ABCD-method materials. Useful pedagogical reference for ABCD and transfer-factor ideas.

---

## 10. Bottom line

For the VBF H→bb problem, the dominant multijet background is best understood as a smooth data-driven continuum under a narrow H→bb peak, with Z→bb treated separately. CMS chooses a direct analytic-fit route; ATLAS chooses a mass-decorrelated ML categorization route that enables a shared data-driven template. These are two complementary answers to the same problem: how to use powerful event categorization without letting QCD modelling uncertainty dominate the Higgs signal extraction.

For broader LHC analyses, there is no universal multijet method. The right method follows from the failure mode that brings QCD into the signal region: smooth continuum, fake object, fake MET, tagger mistag, or classifier-induced sculpting. A good analysis makes that failure mode explicit, derives as much as possible from data, and validates the extrapolation with closure tests and control regions.
