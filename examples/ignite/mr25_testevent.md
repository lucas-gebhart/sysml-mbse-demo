# Simulated test event: MR - 25 Effective IR Resolution Distance

> The Berserker EO/IR sensor shall provide an effective resolution of at least 700 meters, ensuring clear identification and targeting capability at that distance.

- Threshold read from the requirement: **>= 700 m** ("at least 700 meters")

- Test procedure (from the model): **Operational Target Damage Assessment Test** — 39 steps across swimlanes Beserker Configuration 1 SUT, Cyber Test Operator, Ground Control Station, Ground Control Station Operator, Range Control, Test Lead
- Information items exchanged: 15 (14 with no attributes)

## Procedure steps (model)

| # | kind | step | lane | in | out |
|---|---|---|---|---|---|
| 1 | start |  |  |  |  |
| 2 | action | Request Range Permission for Damage Assessment | Test Lead |  | Range Berserker Re-approach Request |
| 3 | action | Verify Range is Ready for Damage Assessment Observation | Range Control | Range Berserker Re-approach Request |  |
| 4 | action | Grant Range Permission for Damage Assessment | Range Control |  | Range BDA Permission |
| 5 | action | Provide Permission to Begin EO/IR Damage Scan | Test Lead | Range BDA Permission | Permission to Begin EO/IR Scans |
| 6 | decision | Cyber Test? | Test Lead |  |  |
| 7 | action | Provide GCS Input for EO/IR Scan Start | Ground Control Station Operator | Permission to Begin EO/IR Scans | EO/IR Scan Start Command GCS Input |
| 8 | action | Provide Permission for EO/IR Spoofing | Test Lead |  | EO/IR Cyber Spoofing Permission |
| 9 | end |  | Test Lead |  |  |
| 10 | action | Transmit EO/IR Scan Command to Berserker | Ground Control Station | EO/IR Scan Start Command GCS Input |  |
| 11 | action | Attempt EO/IR Spoofing/Manipulation | Cyber Test Operator | EO/IR Cyber Spoofing Permission | Cyber EO/IR Spoofing Affect |
| 12 | action | Conduct Routine EO/IR Scene Scan | Beserker Configuration 1 SUT |  |  |
| 13 | action | Provide EO/IR Scan Map and Details to GCS Operator | Ground Control Station |  | EO/IR Scan Map |
| 14 | action | View EO/IR Map for Target Emission Impact | Ground Control Station Operator | EO/IR Scan Map |  |
| 15 | decision |  | Ground Control Station Operator |  |  |
| 16 | action | Inform TL of Reduced Target Signature | Ground Control Station Operator |  | Reduced Target Signature Notification |
| 17 | action | Inform TL of non-impacted Signature | Ground Control Station Operator |  | Non Impacted Target Signature Notification |
| 18 | action | Log Preliminary Non-Impact of Munition | Test Lead | Reduced Target Signature Notification |  |
| 19 | action | Log Preliminary EO/IR Damage Evidence | Test Lead | Non Impacted Target Signature Notification |  |
| 20 | merge |  | Test Lead |  |  |
| 21 | decision | Cyber Test | Test Lead |  |  |
| 22 | merge |  | Test Lead |  |  |
| 23 | action | Log EO/IR Cyber Spoofing Test Result | Test Lead |  |  |
| 24 | action | Provide Permission to Begin Live Video Feed and Approach Target | Test Lead |  | Live Video Feed Permission |
| 25 | action | Input Command for Live Video Feed | Ground Control Station Operator | Live Video Feed Permission | Live Video Feed GCS Command Input |
| 26 | action | Transmit Live Video Feed Command to Berserker | Ground Control Station | Live Video Feed GCS Command Input | DT 12 - Video Feed Start/Stop Command |
| 27 | action | Provide Live Video Feed | Beserker Configuration 1 SUT |  |  |
| 28 | action | Provide Live Video Feed to GCS Operator | Ground Control Station |  | Live Video Feed Visualization Data |
| 29 | action | Observe Target Through Live Video | Ground Control Station Operator | Live Video Feed Visualization Data |  |
| 30 | action | Notify TL of Target Visual Status | Ground Control Station Operator |  |  |
| 31 | action | Log Live Video Functionality Result | Test Lead |  |  |
| 32 | action | Request Range Assessment of Tagrget | Test Lead |  | Range Request for Actual BDA |
| 33 | action | Provide Independent Assessment | Range Control |  | Actual BDA Results |
| 34 | action | Log Range Assessment | Test Lead | Actual BDA Results |  |
| 35 | end |  | Test Lead |  |  |
| 36 | action | Determine if Target Destruction Evidence is Sufficient | Test Lead |  |  |
| 37 | action | Log Operational Damage Assessment Result | Test Lead |  |  |
| 38 | event | Flight TEst Concluded | Test Lead |  |  |
| 39 | end |  |  |  |  |

## Measure of Performance

Effective identification range R90: slant range at which P(identify) = 0.9 from a logistic fit of per-pass outcomes; 90 % bootstrap CI.

| condition | passes | identified | R90 (m) | 90 % CI | meets threshold |
|---|---|---|---|---|---|
| all conditions | 240 | 208 | 790 | 728–864 | yes |
| day / clear | 60 | 55 | 902 | 782–1146 | yes |
| day / haze | 60 | 50 | 732 | 633–843 | no |
| night / clear | 60 | 52 | 789 | 694–956 | no |
| night / haze | 60 | 51 | 762 | 630–914 | no |

**Verdict: INCONCLUSIVE** — Pooled data meets the threshold but the 90 % lower bound does not in day / haze, night / clear, night / haze (point estimates do; the per-condition sample is too small to bound R90); the requirement does not state the conditions under which 'effective resolution' is to be achieved, so the verdict cannot be arbitrated.

## Observed P(ID) by range bin

| range (m) | passes | identified | P(ID) |
|---|---|---|---|
| 300–400 | 14 | 14 | 1.00 |
| 400–500 | 23 | 23 | 1.00 |
| 500–600 | 20 | 20 | 1.00 |
| 600–700 | 49 | 47 | 0.96 |
| 700–800 | 54 | 49 | 0.91 |
| 800–900 | 19 | 14 | 0.74 |
| 900–1000 | 25 | 19 | 0.76 |
| 1000–1100 | 12 | 10 | 0.83 |
| 1100–1200 | 9 | 6 | 0.67 |
| 1200–1300 | 15 | 6 | 0.40 |

## What the model is missing to make this a real verification

- **[error]** threshold 'at least 700 meters' has no Measure of Performance in the model → Add a MOP value property (e.g. 'effective identification range : m') to the verifying TestCase or a «TestObjective», with the measurement method (P(ID) ≥ 0.9 from per-pass identification outcomes) and the acceptance criterion >= 700 m.
- **[error]** 14 of 15 information items exchanged by the procedure have no attributes (Range Berserker Re-approach Request, Range BDA Permission, Permission to Begin EO/IR Scans, EO/IR Scan Start Command GCS Input …) → Give the «ResourceInformation» classes the fields the test actually records (slant range, condition, identification outcome, time to identify, spoof detected) so the log format is defined by the model, not by the test team on the day.
- **[warn]** 6 'Log …' steps but no UTP «TestLog» / «Verdict» elements anywhere in the test model → Add a «TestLog» per execution with «TestLogEntry»s produced by the Log steps and a Verdict typed by the UTP Verdict enumeration, so results are model elements the RVTM can read.
- **[error]** MR - 25 is refined by the procedure's activities but has no «Verify» relationship → Add Verify from 'Operational Target Damage Assessment Test' (or its owning TestCase) to MR - 25 Effective IR Resolution Distance.
- **[warn]** requirement does not state test conditions (illumination, visibility, target class, aspect) → Add the conditions as constraint properties or a «TestObjective» so the verdict is arbitrable when day and night results disagree.

_Synthetic data: 240 passes generated with a notional sensor model (notional EO/IR (no performance properties in the product model)); nothing here is a measured MQ-99 result._