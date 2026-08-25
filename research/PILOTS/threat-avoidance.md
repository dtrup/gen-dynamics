# Pilot: Human Threat Interpretation and Avoidance

## Status

Active. Exploratory and not publication ready.

## Scope

Test whether changing the interpreted meaning of an ambiguous situation reorganizes actionable possibilities and avoidance beyond lower-level conditioned-response accounts.

## Claims under test

- C-001: core semantic-field loop.
- C-002: semantic causal invariance.
- C-003: incremental value of the effective field.
- C-004: semantic attractor regimes.
- C-005: historical recursion.

## Rival explanations

- Conditioned defensive responses explain avoidance without semantic variables.
- Attention, valuation, confidence, and action selection suffice without an effective-field construct.
- Repetition reflects habit or reinforcement rather than attraction.

## Evidence ledger

Roles are `[review]`, `[direct]`, `[rival]`, and `[methods]`. Use one row per unique DOI or stable URL.

| Source ID | Role | Citation and stable URL | Evidence type | Relevant finding | Limitation | Claims |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-TA-001 | [review] [rival] | Mertens, G., Boddez, Y., Sevenster, D., Engelhard, I. M., & De Houwer, J. (2018). A review on the effects of verbal instructions in human fear conditioning. *Biological Psychology, 137*, 49–64. https://doi.org/10.1016/j.biopsycho.2018.07.002 | Review; abstract and PubMed metadata inspected, not full text | Verbal instructions can establish fear without CS–US pairings and can moderate pairing-based fear; the review also evaluates multiple mental-process accounts. | Abstract-level inspection does not establish which account best fits each outcome, and laboratory fear responses are not equivalent to broad actionable fields. | C-001, C-002 |
| SRC-TA-002 | [direct] | Javanbakht, A., Duval, E. R., Cisneros, M. E., Taylor, S. F., Kessler, D., & Liberzon, I. (2017). Instructed fear learning, extinction, and recall: Additive effects of cognitive information on emotional learning of fear. *Cognition and Emotion, 31*(5), 980–987. https://doi.org/10.1080/02699931.2016.1169997 | Randomized laboratory experiment (N=40); abstract and PubMed metadata inspected, not full text | Contingency information enhanced fear expression, safety information facilitated extinction and recall, and omission before recall produced renewal. | Small healthy-participant study; information was embedded in the conditioning context, so the design does not isolate semantic content from expectancy or context. | C-001, C-002, C-004 |
| SRC-TA-003 | [direct] [methods] | Pittig, A., & Wong, A. H. K. (2021). Incentive-based, instructed, and social observational extinction of avoidance: Fear-opposite actions and their influence on fear extinction. *Behaviour Research and Therapy, 137*, 103797. https://doi.org/10.1016/j.brat.2020.103797 | Four-group randomized avoidance experiment (N=160); abstract and PubMed metadata inspected, not full text | Instructions and incentives strongly reduced instrumental avoidance despite high fear and initiated fear extinction; observation reduced fear more directly but avoidance only moderately. | The intervention contrasts differ in information, incentive, and social pathway; no meaning-preserving carrier manipulation or out-of-sample semantic model comparison was reported. | C-001, C-002 |
| SRC-TA-004 | [rival] [methods] | Mertens, G., Braem, S., Kuhn, M., Lonsdorf, T. B., van den Hout, M. A., & Engelhard, I. M. (2018). Does US expectancy mediate the additive effects of CS–US pairings on contingency instructions? *Behaviour Research and Therapy, 110*, 41–46. https://doi.org/10.1016/j.brat.2018.09.003 | Within-subject mediation/path analysis across subjective, startle, and neural measures; abstract and PubMed metadata inspected, not full text | CS–US pairings added to instructed effects across fear, startle, and neural pattern measures; US expectancy did not mediate these additions, while exploratory analyses implicated subjective fear. | Reanalysis/mediation cannot identify a uniquely semantic cause; the failure of one expectancy mediator leaves associative and other lower-level accounts open. | C-001, C-002 |

## Scorecard

| Dimension | Score 0–4 | Reason |
| --- | ---: | --- |
| Semantic necessity | 1 | Instructions change fear and avoidance, but expectancy, contextual, motivational, and associative descriptions remain viable. |
| Operational measurability | 2 | Randomized instructions, incentives, observation, expectancy, fear, startle, avoidance, and neural patterns provide a workable multilevel battery. |
| Rival discrimination | 1 | Additive pairing effects and dissociations among fear and avoidance constrain a purely instructional account but do not compare carrier-invariant semantic models with matched lower-level models. |
| Perturbation specificity | 2 | Instructions and incentives perturb avoidance, and contingency information perturbs acquisition, extinction, and recall; semantic content is not independently crossed with carrier. |
| Evidence quality | 1 | The ledger has a review and three relevant experiments/analyses, but this run inspected abstracts rather than full texts and includes overlapping authorship. |

## RUN-002 comparison

The bounded result is **pathway plurality, not semantic necessity**. Instructed contingency information can alter fear acquisition, extinction, recall, and instrumental avoidance, so a conditioned-response account restricted to experienced CS–US pairings is inadequate. The avoidance study is especially discriminating because instructions and incentives reduced action while fear remained high, whereas observation reduced fear more directly but changed avoidance less. Fear and avoidance therefore cannot be treated as one undifferentiated conditioned output.

The evidence does not yet earn a distinct semantic causal variable. Instructions can be represented as expectancy updates or contextual cues; incentives alter action value; observation conveys outcome information; and subsequent CS–US pairings add effects beyond prior instructions. The mediation result rules against US expectancy as a complete mediator of those additive pairing effects, but it does not rule out associative history, subjective fear, attention, valuation, or other component variables.

For C-002, the next decisive design must cross **interpreted content** with **physical carrier** while measuring experienced contingencies and component variables. Meaning-equivalent instructions delivered through different carriers should generalize, while physically similar carriers assigned different meanings should diverge. The semantic grouping must then improve held-out prediction or intervention selection over expectancy, fear, action value, attention, and learning-history models.

## Falsifiers

- Semantic reframing adds no predictive information after conditioned history and physical stimulation are controlled.
- A component-variable model performs as well as an effective-field representation out of sample.
- Avoidance persistence lacks perturbation recovery, switching, or entry/exit asymmetry.

## Residual uncertainty

- Whether instruction effects generalize across meaning-preserving carrier changes is unresolved.
- Whether interpreted content predicts avoidance beyond expectancy, fear, action value, attention, and conditioning history is unresolved.
- Abstract-only inspection limits assessment of manipulation checks, exclusions, effect sizes, analytic flexibility, and exact temporal ordering.
- Healthy laboratory samples and short-horizon avoidance tasks may not generalize to persistent clinical threat avoidance.

## Run log

- RUN-002 planned: semantic intervention versus conditioned-response rivals.
- RUN-003 planned: effective field, feedback, perturbation, and hysteresis.
- RUN-002 source-selection pass: selected four DOI-deduplicated sources spanning review, direct intervention, rival, and measurement roles; inspection was limited to abstracts and authoritative PubMed metadata.
- RUN-002 analytical pass: rejected a pairing-only rival, retained broader component and associative rivals, and specified a carrier-by-content test with held-out model comparison.
