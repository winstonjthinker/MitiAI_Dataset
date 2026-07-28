# Target population and sampling

**ZW-BioBank · Minimum Expectations §4.8**

There are **two target populations**, and they are sampled differently. Treating them as one is the
commonest way a dataset like this misrepresents itself.

---

## Population A — biological material

**Frame.** Soil, bark, root, plant tissue, fungus and water from three Zimbabwean ecozones:
Eastern Highlands (montane cloud forest), Mazowe (semi-arid), Zvishavane.

**Design.** Stratified by ecozone and season, with a quota:

| Ecozone | Quota | Rationale |
|---|---|---|
| Eastern Highlands | 200 | Highest floristic diversity; also the closest to institutions, so the quota is a **ceiling** rather than a target |
| Mazowe | 150 | Distinct arid-adapted chemistry; the least accessible |
| Zvishavane | 150 | The dominant Zimbabwean woodland type; large microbial reservoir |

**Both seasons are mandatory.** Plant and microbial chemistry differ between wet and dry, so a
single-season dataset confounds season with site. Every record carries a `season` tag and the
validator raises a warning for any ecozone that has only one.

**Is it representative?** Of these three ecozones under the stated quota, yes. Of Zimbabwe, no —
and it is not claimed to be. Phase I is a 500-sample pilot, not a national inventory.

---

## Population B — traditional knowledge holders

**Frame.** Holders who (a) live in a participating community, (b) whose council has issued an
endorsement, and (c) who give free, prior and informed consent.

**Design.** Not a probability sample. Holders are approached through community councils, and
participation is entirely voluntary at both the council and the individual level.

> **This corpus is not a representative sample of Zimbabwean traditional knowledge and cannot be
> made into one.**

It carries the selection bias of who agreed to speak. It is skewed toward:

- communities whose councils chose to engage;
- holders comfortable being recorded, even pseudonymously;
- knowledge the holder considers shareable — sacred knowledge is absent **by design**, and its
  absence is recorded as a refusal event rather than left invisible.

Stating this plainly is worth more than any mitigation we could claim. A reviewer who finds an
undisclosed limitation stops trusting everything else in the package.

**What we do instead of claiming representativeness:**

| Measure | Mechanism |
|---|---|
| A 30% floor on Ndebele-language records | Checked by the validator on every batch, not asserted annually |
| Community-level attribution by default | District and ward; named attribution is explicit opt-in |
| Refusals counted | Every boundary drawn is recorded with no content, so the exclusion is auditable |
| Coverage published | `v_bias_coverage` computes the position from the data; the deficit is visible to anyone |

---

## Coverage gaps we know about

| Gap | Effect | Disclosed where |
|---|---|---|
| Protected-area access not secured | Phase I is anchored on communal land, over-representing human-modified habitat | `source_register.csv` `known_limitations` |
| Season not yet balanced in every ecozone | Season confounded with site until the second pass | Validator warning, held open |
| Shona-speaking communities more accessible | Ndebele share monitored against a floor | `bias_risk_register.csv` BR-03 |
| Western-built spectral libraries | The compounds they cannot match are exactly the novel fraction sought | Unannotated features retained rather than discarded |
| Herbarium backlog | Some identifications remain field-tentative | `taxon_confidence` separates the three levels |

---

## Sample size, and why 500

500 environmental samples is what one mobile laboratory and one LC-MS instrument can process to a
defensible standard within the Phase I window, at the preservation latency the mobile laboratory
makes possible. It is a **capacity-derived** figure, not a power calculation, and is described as
such rather than dressed up as one.

A larger number would either exceed the processing capacity — producing degraded samples and
untrustworthy metabolomics — or require dropping the preservation standard that makes the dataset
worth building.
