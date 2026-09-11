# Pilot: Pavlovian Fear Conditioning as a Hostile Boundary Case

## Status

Complete. Exploratory and not publication ready.

## Scope

Construct the strongest lower-level explanation of Pavlovian fear conditioning and determine when semantic description is unnecessary, optional, or warranted.

## Claims under test

- C-002: semantic causal invariance.
- C-004: semantic attractor regimes.
- C-007: typed cross-scale comparison.

## Rival explanations

- Associative learning, prediction error, defensive circuits, and reinforcement fully explain the observed dynamics.
- Apparent semantic organization is retrospective anthropomorphic description.
- Persistence reflects plasticity and habit rather than a semantic attractor.

## Evidence ledger

Roles are `[review]`, `[direct]`, `[rival]`, and `[methods]`. Use one row per unique DOI or stable URL.

| Source ID | Role | Citation and stable URL | Evidence type | Relevant finding | Limitation | Claims |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-FC-001 | [review] [rival] | LeDoux, J. E. (2014). Coming to terms with fear. *Proceedings of the National Academy of Sciences, 111*(8), 2871–2878. https://doi.org/10.1073/pnas.1400335111 | Conceptual neuroscience review; full text inspected via PubMed Central | Pavlovian threat conditioning can be described as nonconscious defensive-circuit learning; defensive responses and conscious fear should not be collapsed into one construct. | The circuit/process distinction bounds semantic interpretation but does not by itself compare predictions from semantic and nonsemantic groupings. | C-002, C-007 |
| SRC-FC-002 | [direct] [rival] | Pearce, J. M., & Hall, G. (1980). A model for Pavlovian learning: Variations in the effectiveness of conditioned but not of unconditioned stimuli. *Psychological Review, 87*(6), 532–552. https://doi.org/10.1037/0033-295X.87.6.532 | Formal associative-learning theory evaluated against conditioning phenomena; bibliographic metadata and accessible abstract/summary inspected, not full text | Associability changes with predictive uncertainty, allowing cue competition and changes in attention-like learning rate to be explained without semantic content. | A behavioural learning model abstracts away neural implementation and may require extensions across all conditioning phenomena; this run does not estimate it on new data. | C-002, C-007 |
| SRC-FC-003 | [direct] [rival] | Johansen, J. P., Diaz-Mataix, L., Hamanaka, H., et al. (2014). Hebbian and neuromodulatory mechanisms interact to trigger associative memory formation. *Proceedings of the National Academy of Sciences, 111*(51), E5584–E5592. https://doi.org/10.1073/pnas.1421304111 | In-vivo optogenetic and electrophysiological rodent experiments; full text inspected via PubMed Central | Convergent conditioned-stimulus activity, aversive-pathway activation, and neuromodulation were jointly necessary and sufficient for synaptic strengthening and an associative defensive memory. | Artificial circuit stimulation and rodent freezing do not exhaust human fear experience, and sufficiency within this preparation does not establish sufficiency for semantic cases. | C-002, C-004, C-007 |
| SRC-FC-004 | [methods] [review] | Lonsdorf, T. B., Menz, M. M., Andreatta, M., et al. (2017). Don’t fear ‘fear conditioning’: Methodological considerations for the design and analysis of studies on human fear acquisition, extinction, and return of fear. *Neuroscience & Biobehavioral Reviews, 77*, 247–285. https://doi.org/10.1016/j.neubiorev.2017.02.026 | Consensus-style methodological review; abstract and PubMed metadata inspected, not full text | Conditioned responding is measure-, phase-, and design-dependent; inference requires explicit terminology, multiple response systems, adequate trials, and analysis choices matched to acquisition or extinction. | Methodological heterogeneity constrains inference but does not choose between associative, circuit, propositional, or semantic explanations. | C-002, C-007 |
| SRC-FC-005 | [review] [rival] | Mitchell, C. J., De Houwer, J., & Lovibond, P. F. (2009). The propositional nature of human associative learning. *Behavioral and Brain Sciences, 32*(2), 183–198. https://doi.org/10.1017/S0140525X09000855 | Target article reviewing evidence for propositional over automatic link-formation accounts; abstract and bibliographic metadata inspected, not full text | Human associative learning can be described as propositional reasoning interacting with memory retrieval and perception rather than automatic formation of associative links. | A propositional representation is not automatically a semantic causal variable; the review does not test carrier invariance or incremental prediction over measured expectancies. | C-002, C-007 |
| SRC-FC-006 | [direct] [methods] | Atlas, L. Y., Doll, B. B., Li, J., Daw, N. D., & Phelps, E. A. (2016). Instructed knowledge shapes feedback-driven aversive learning in striatum and orbitofrontal cortex, but not the amygdala. *eLife, 5*, e15192. https://doi.org/10.7554/eLife.15192 | Human instruction-by-reinforcement experiment with computational modelling and fMRI; full text inspected via PubMed Central | Instructions changed expectancy-related learning signals in striatum and orbitofrontal cortex, while amygdala responses continued to track reinforcement similarly across groups. | Circuit dissociation shows that instruction is not a unitary semantic cause, and the design does not vary physical carrier while preserving interpreted content. | C-002, C-007 |
| SRC-FC-007 | [direct] | Mertens, G., Boddez, Y., Krypotos, A.-M., & Engelhard, I. M. (2021). Human fear conditioning is moderated by stimulus contingency instructions. *Biological Psychology, 158*, 107994. https://doi.org/10.1016/j.biopsycho.2020.107994 | Randomized three-group human conditioning experiment (N=102); abstract and PubMed metadata inspected, not full text | Precise or discovery instructions facilitated acquisition and awareness relative to no instructions, and reversal instructions immediately reversed conditioned skin-conductance and startle responses. | Instructions, awareness, and expectancy were not independently manipulated; immediate reversal does not establish carrier-invariant semantic grouping beyond propositional contingency knowledge. | C-002, C-007 |
| SRC-FC-008 | [direct] [rival] | Braem, S., De Houwer, J., Demanet, J., Yuen, K. S. L., Kalisch, R., & Brass, M. (2017). Pattern analyses reveal separate experience-based fear memories in the human right amygdala. *Journal of Neuroscience, 37*(34), 8116–8130. https://doi.org/10.1523/JNEUROSCI.0908-17.2017 | Two human fMRI pattern-analysis experiments; full text inspected via PubMed Central | With instructed contingencies held constant, right-amygdala patterns distinguished instructed-plus-experienced from merely instructed contingencies across stimulus categories. | Neural-pattern separation does not show which representation controls behaviour and does not directly compare a semantic model with expectancy and experience-history models. | C-002, C-007 |

## Scorecard

| Dimension | Score 0–4 | Reason |
| --- | ---: | --- |
| Semantic necessity | 1 | Standard cue–outcome learning and defensive responding have a strong nonsemantic account; this run does not test instruction or carrier-invariant meaning. |
| Operational measurability | 4 | Trials, carrier and content, instructions, awareness, expectancy, reinforcement history, autonomic and behavioural responses, and circuit signals can be crossed and measured separately. |
| Rival discrimination | 4 | Associative, propositional, reinforcement, experience-history, and circuit accounts make distinct predictions; none of the selected studies demonstrates semantic incremental value over all of them. |
| Perturbation specificity | 3 | Cue–outcome schedules and optogenetic manipulation isolate learning inputs and circuit mechanisms; translation from artificial stimulation to natural human learning remains limited. |
| Evidence quality | 3 | Eight sources cover theory, review, methods, randomized instruction, computational modelling, causal circuit intervention, and neural patterns; four full texts were inspected, with author and paradigm overlap remaining. |

## RUN-004 lower-level account

The strongest bounded account separates three explanatory levels. At the **computational-learning level**, prediction and uncertainty change associative strength and cue associability across trials. At the **mechanistic level**, convergent cue activity, aversive-pathway input, neuromodulation, and synaptic plasticity alter defensive circuits. At the **measurement level**, freezing, startle, skin conductance, expectancy, and reported fear are distinct outputs whose convergence cannot be assumed. Together these levels explain acquisition, cue competition, extinction-related change, and defensive responding without treating the conditioned cue as a semantic object.

Johansen and colleagues supply the sharpest intervention evidence in this pass: paired activity and neuromodulation were manipulated to test necessity and sufficiency for synaptic strengthening and associative defensive memory. Pearce–Hall supplies a lower-level account of why learning changes with predictive uncertainty. LeDoux blocks an invalid cross-scale inference: a defensive circuit that detects and responds to threat is not thereby a mechanism for conscious fear. Lonsdorf and colleagues make the corresponding measurement constraint explicit by treating response systems, phases, and analysis choices separately.

This account sets a **nonsemantic default boundary** for standard Pavlovian preparations. When outcomes are explained by physical cue identity, experienced contingency, prediction error or associability, circuit plasticity, and response-specific measurement, semantic description is optional shorthand rather than an additional cause. A semantic account would have to improve intervention or held-out prediction across meaning-preserving carrier changes after those variables are controlled; none of the RUN-004 studies performs that test.

The boundary is not a universal rejection of semantic control. Rodent circuit sufficiency for a defensive response does not explain conscious fear, instructed contingency learning, or carrier-invariant interpretation. RUN-005 must therefore test whether any such cases require semantic grouping rather than merely adding propositional vocabulary to an associative or circuit account.

## RUN-005 semantic boundary

RUN-005 narrows the boundary but does not establish semantic necessity. Contingency instructions causally alter acquisition and can immediately reverse conditioned responses. Instructions also change learning-related signals in striatum and orbitofrontal cortex. These results rule out an account restricted to experienced cue–outcome pairings and show that represented contingency information can enter the control of human defensive learning.

Three findings prevent the stronger inference. First, propositional contingency knowledge can explain instruction effects without assuming that a broader semantic grouping has independent causal status. Second, instruction and reinforcement dissociate across neural systems: amygdala responses can continue to track reinforcement when striatal and orbitofrontal signals update with instructions. Third, with instructed contingency held constant, experience leaves distinguishable amygdala patterns. Interpreted content therefore neither replaces learning history nor acts as one undifferentiated system-wide variable.

The resulting boundary has three zones:

1. **Unnecessary:** In standard Pavlovian defensive preparations, physical cue identity, experienced contingency, associability or prediction, circuit plasticity, and response-specific measures provide the default explanation.
2. **Optional shorthand:** Where instruction effects are fully captured by explicit expectancy or propositional contingency knowledge, semantic language may summarize represented content but has not added an independently supported cause.
3. **Potentially warranted but untested:** Semantic grouping would earn causal status only if meaning-equivalent instructions generalize across physically different carriers, physically similar carriers with different interpreted content diverge, and content grouping improves held-out behavioural or intervention prediction beyond expectancy, awareness, reinforcement history, and circuit or component measures.

No RUN-005 study jointly crosses carrier and content or performs that held-out comparison. The evidence therefore operationalizes C-002 rather than confirming it. It also preliminarily tests C-007: treating instruction, proposition, defensive circuitry, conscious fear, and semantic content as interchangeable would erase observed response- and circuit-specific dissociations.

## Falsifiers

- Lower-level variables predict interventions and generalization without semantic grouping.
- Meaning-like descriptions add no invariant grouping across physical carriers.
- The architecture cannot specify a nonsemantic boundary without ad hoc exceptions.

## Residual uncertainty

- The selected lower-level account has not been compared out of sample with propositional or semantic models.
- Two sources were inspected only at abstract or summary level, limiting assessment of model exceptions and methodological recommendations.
- Rodent circuit interventions establish a mechanism for defensive learning in their preparation, not a complete account of conscious human fear.
- No selected study jointly manipulates physical carrier and interpreted content while matching expectancy and reinforcement history.
- Propositional knowledge may be an adequate rival description of instruction effects; its relation to semantic content remains theoretically contested rather than empirically separated here.
- Neural dissociations constrain system-wide interpretations but do not by themselves identify which representation controls behaviour.

## Run log

- RUN-004 planned: strongest lower-level account.
- RUN-005 planned: semantic boundary and required revisions.
- RUN-004 source-selection pass: added four DOI-deduplicated sources covering defensive-circuit terminology, associability theory, causal circuit intervention, and human conditioning methodology; two full texts and two abstract-level records were inspected.
- RUN-004 analytical pass: constructed a computational-learning, circuit-plasticity, and response-measurement account; set nonsemantic explanation as the default for standard Pavlovian preparations while reserving instruction and carrier invariance for RUN-005.
- RUN-005 source-selection pass: added four DOI-deduplicated sources covering propositional theory, instruction-by-reinforcement modelling, contingency-instruction intervention, and experience-sensitive neural patterns; two full texts and two abstract-level records were inspected.
- RUN-005 analytical pass: divided the boundary into nonsemantic default, optional propositional shorthand, and untested carrier-invariant semantic causation; operationalized C-002 and preliminarily tested C-007 without changing protected synthesis text.
