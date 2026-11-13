# Project Audit | 13 November 2026

**Repository:** Sonkhe-Shongwe/banking-fraud-intelligence  
**Audited revision:** main at 6326968c832a1780119934fbf6036b88097bab11  
**Audit type:** Documentation, analytical continuity, P5 readiness and repository governance review  
**Scope limitation:** This audit inspected the remote GitHub main branch. It did not inspect the owner's current local working tree or execute the local Power BI Desktop application.

## 1. Executive verdict

The analytical foundation is documented and the project is correctly positioned at 72% overall, with P1 at 80% and P2–P4 complete. The P4 September rank export has been generated and confirmed by the owner in Windows.

The project is **not yet ready for Power BI implementation** because the detailed visual specification and page wireframes still require owner approval. The report folder is empty, which is consistent with P5 remaining at 0%. The most important documentation defect was a stale dark-theme statement in the handoff after the owner approved the Premium Banking Intelligence light-theme direction.

The data source is simulated. Publication permissions for source data and derived artefacts remain unresolved. That boundary must remain in force.

## 2. Verified repository snapshot

| Item | Observed state |
|---|---|
| Default branch | main |
| Audited HEAD | 6326968c832a1780119934fbf6036b88097bab11 |
| Latest commit at audit | Document local notebook runs and align the P5 handoff |
| Branch protection | Disabled on main at audit time |
| Required status checks | None configured on main at audit time |
| P1 | 80% |
| P2 | 100% |
| P3 | 100% |
| P4 | 100% |
| P5 | 0% |
| P6 | 0% |
| Overall | 72% |
| Power BI directory | Contains only .gitkeep; no report or theme file is present |
| Assets and reports directories | Reserved placeholders; no committed design-board image or report output was found in the inspected tree |

The 72% arithmetic is correct: P1 contributes 12 weighted points and P2–P4 contribute 60 points.

## 3. Audit findings

| ID | Severity | Finding | Status / action |
|---|---|---|---|
| AUD-01 | High | The handoff described the proposed report as dark-themed, conflicting with the owner's later approval of Direction A, Premium Banking Intelligence. | Corrected in the current handoff and design system. |
| AUD-02 | Medium | The handoff described the two-page scope as awaiting approval even though the owner had approved Fraud Overview and Review Policy Comparison. | Corrected; page scope is now recorded as approved. |
| AUD-03 | High | No authoritative Power BI design system or visual acceptance standard existed. | Added this design-system document. Detailed tokens and wireframes remain subject to owner approval. |
| AUD-04 | High | The generated concept board contains illustrative values and dimensions that are not in the dataset. | Explicitly labelled as moodboard-only. Its sample metrics must not enter the report. |
| AUD-05 | High | The data does not support loss prevented, alerts reviewed, confirmed outcomes, turnaround time, geography, channel, product or customer-segment claims. | Added a supported-metric contract and prohibited-claim list to the design system. |
| AUD-06 | High | Source-data reuse and publication rights for derived artefacts remain unresolved. | Open. Keep raw, processed, row-level and report-embedded transaction data local until cleared. |
| AUD-07 | Medium | The P4 export contains retrospective labels and an uncalibrated logistic-regression decision score. | Recorded correct metric language; do not display the decision score as a probability. |
| AUD-08 | Medium | The restricted cohort uses independently recalculated rank columns. A naive filter on the full-population ranks would produce incorrect review queues. | Added an explicit report rule: use restricted ranks for the at-or-below-220 cohort. |
| AUD-09 | Medium | No Power BI report, theme JSON, DAX measure dictionary or desktop validation evidence exists yet. | Expected at P5 0%; build only after design approval. Reconciliation and interaction tests are P5 acceptance gates. |
| AUD-10 | Low | Main is not protected and has no required status checks. | Governance improvement to consider separately; no branch settings changed in this audit. |
| AUD-11 | Informational | The audit cannot determine whether the owner's local notebooks, generated files or uncommitted changes are clean. | Local state remains to be checked in GitHub Desktop/VS Code. |

## 4. Data and modelling constraints confirmed by the source audit

The pinned source audit records 183 daily batches from 1 April through 30 September 2018, containing 1,754,155 simulated transactions and 14,681 fraud labels (0.837%). It records no missing field values or duplicate transaction IDs, 42 zero-amount transactions, and 231,973 rows that share a timestamp with at least one other row.

All 3,258 transactions above amount 220 are labelled fraud in this simulator. The source has no fraud-confirmation timestamp. These facts affect interpretation and must be visible in the dashboard methodology note.

The P4 export contains 287,873 September rows. It provides event time, amount, retrospective fraud label, model decision score and four one-based daily ranks: two policies across the full population and two policies within the amount-at-or-below-220 cohort.

The logistic-regression score is a ranking score, not a calibrated probability. The sum of amounts on selected fraud-labelled rows is not a measured loss, saving or prevented loss.

## 5. Documentation consistency review

| Record | Audit result |
|---|---|
| README | Project purpose and Python/PBI split are clear; P5 owner decisions needed to be stated more precisely. Updated. |
| Documentation index | Core documents are discoverable; design system and audit entries were missing. Updated. |
| Master continuation prompt | Approval boundaries and evidence workflow are strong; it needed the latest design decision and design-system reference. Updated. |
| Project scorecard | Phase arithmetic and current 72% total are correct. P5 remains 0%. Updated next gate. |
| Session handoff | Strong continuity record, but contained the stale dark-theme and pending-page-scope statements. Corrected. |
| Data source audit | Source revision, quality, simulator rule and publication caveat are recorded. Retained. |
| Data model | Grain, fields, feature logic and P4 export ranks are recorded. Retained. |
| Methodology | Chronological evaluation, fixed review capacity and reporting evidence are recorded. Retained. |
| Findings | It described how to reproduce September results but lacked the concise aggregate comparison table. Updated. |
| Local data guide | Windows workflow, notebook execution and pull recovery are documented. Retained. |
| Power BI folder | Empty placeholder only. This is not a defect before P5 implementation. |

## 6. Decisions now recorded as authoritative

1. Power BI Desktop is the approved dashboard platform.
2. The first report contains two approved pages: Fraud Overview and Review Policy Comparison.
3. The first implementation target is Review Policy Comparison.
4. The approved visual direction is A — Premium Banking Intelligence, with a light and restrained visual identity.
5. The owner requires approval before major design changes or implementation of unapproved visual decisions.
6. The generated concept board is inspiration only and its displayed sample metrics are not project data.
7. Publication clearance is separate from design and implementation approval.

The palette, typography, exact canvas/grid, wireframes, chart selection, card treatments and interaction details remain proposals until reviewed and approved.

## 7. Required next actions

| Priority | Action | Closure evidence |
|---|---|---|
| 1 | Review and approve or revise the proposed colour tokens and typography | Owner decision recorded in design system |
| 2 | Present and approve the two page wireframes | Owner-approved page layouts and chart choices |
| 3 | Create and import the Power BI theme | Successful import and visual inspection in Power BI Desktop |
| 4 | Build the approved pages | Local PBIX/report with supported metrics only |
| 5 | Reconcile report measures | Power BI matches Python for all eight September policy/cohort/capacity cases and representative date selections |
| 6 | Test interactions and accessibility | Filter, navigation, tooltip, tab-order and contrast checks recorded |
| 7 | Resolve publication scope | Source and derived-artifact permissions documented before release |

## 8. Audit closeout

This audit closes the documentation inconsistency and establishes a formal design-governance baseline. It does **not** close P1 publication scope, does not increase P5 progress, does not create a Power BI report and does not authorise the proposed palette or wireframes as final.

**Next checkpoint:** Owner review of the detailed design system and page wireframes. Keep overall project progress at 72% until new phase evidence meets the scorecard criteria.
