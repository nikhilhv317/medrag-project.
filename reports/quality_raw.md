# Data quality report: raw

Generated 2026-10-27 14:26

## Row counts

- **patients**: 20,316
- **conditions**: 35,417
- **studies**: 92,944
- **ai_analysis**: 91,528
- **reports**: 92,935

Study dates: 2020-10-02 00:43:00 to 2029-03-19 00:00:00

## Checks

| Table | Check | Rows | % | Status |
|---|---|---:|---:|---|
| patients | duplicate patient_id | 0 | 0.0 | OK |
| patients | duplicate MRN (same person, several ids) | 622 | 3.06 | WARN |
| patients | duplicate name + date of birth | 614 | 3.02 | WARN |
| patients | name has stray whitespace or wrong case | 656 | 3.23 | WARN |
| patients | test / dummy record | 5 | 0.02 | ERROR |
| patients | missing name | 0 | 0.0 | OK |
| patients | non-standard gender value | 694 | 3.42 | WARN |
| patients | missing date of birth | 196 | 0.96 | WARN |
| patients | date of birth in the future | 66 | 0.32 | ERROR |
| studies | duplicate study row | 1,416 | 1.52 | ERROR |
| studies | duplicate study_id | 1,416 | 1.52 | ERROR |
| studies | orphan (patient does not exist) | 567 | 0.61 | ERROR |
| studies | non-standard modality | 29,846 | 32.11 | WARN |
| studies | non-standard priority | 2,826 | 3.04 | WARN |
| studies | missing study date | 609 | 0.66 | ERROR |
| studies | study date in the future | 524 | 0.56 | ERROR |
| studies | missing body part | 0 | 0.0 | OK |
| reports | orphan (study does not exist) | 0 | 0.0 | OK |
| reports | empty report text | 858 | 0.92 | ERROR |
| reports | contains HTML markup | 2,687 | 2.89 | WARN |
| reports | duplicate report for same study | 2,814 | 3.03 | WARN |
| reports | non-standard status | 2,847 | 3.06 | WARN |
| reports | missing IMPRESSION section | 26 | 0.03 | WARN |
| ai_analysis | orphan (study does not exist) | 0 | 0.0 | OK |
| ai_analysis | missing confidence | 855 | 0.93 | WARN |
| ai_analysis | confidence outside 0-1 | 3,468 | 3.79 | ERROR |
| ai_analysis | studies without AI analysis | 0 | 0.0 | OK |

**9 error checks failing.**