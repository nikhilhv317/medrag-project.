# Data quality report: clean

Generated 2026-10-27 14:26

## Row counts

- **patients**: 20,000
- **conditions**: 35,417
- **studies**: 89,868
- **ai_analysis**: 89,868
- **reports**: 89,014

Study dates: 2020-10-02 00:43:00 to 2026-09-29 23:30:00

## Checks

| Table | Check | Rows | % | Status |
|---|---|---:|---:|---|
| patients | duplicate patient_id | 0 | 0.0 | OK |
| patients | duplicate MRN (same person, several ids) | 0 | 0.0 | OK |
| patients | duplicate name + date of birth | 0 | 0.0 | OK |
| patients | name has stray whitespace or wrong case | 0 | 0.0 | OK |
| patients | test / dummy record | 0 | 0.0 | OK |
| patients | missing name | 0 | 0.0 | OK |
| patients | non-standard gender value | 0 | 0.0 | OK |
| patients | missing date of birth | 252 | 1.26 | WARN |
| patients | date of birth in the future | 0 | 0.0 | OK |
| studies | duplicate study row | 0 | 0.0 | OK |
| studies | duplicate study_id | 0 | 0.0 | OK |
| studies | orphan (patient does not exist) | 0 | 0.0 | OK |
| studies | non-standard modality | 0 | 0.0 | OK |
| studies | non-standard priority | 0 | 0.0 | OK |
| studies | missing study date | 0 | 0.0 | OK |
| studies | study date in the future | 0 | 0.0 | OK |
| studies | missing body part | 0 | 0.0 | OK |
| reports | orphan (study does not exist) | 0 | 0.0 | OK |
| reports | empty report text | 0 | 0.0 | OK |
| reports | contains HTML markup | 0 | 0.0 | OK |
| reports | duplicate report for same study | 0 | 0.0 | OK |
| reports | non-standard status | 0 | 0.0 | OK |
| reports | missing IMPRESSION section | 0 | 0.0 | OK |
| ai_analysis | orphan (study does not exist) | 0 | 0.0 | OK |
| ai_analysis | missing confidence | 1,640 | 1.82 | WARN |
| ai_analysis | confidence outside 0-1 | 0 | 0.0 | OK |
| ai_analysis | studies without AI analysis | 0 | 0.0 | OK |

**All error-level checks pass.**