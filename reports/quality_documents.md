# Document quality report

| Check | Before | After |
|---|---:|---:|
| empty text | 61 | 0 |
| very short (< 15 words) | 99 | 0 |
| duplicate document (same text, same source) | 2,643 | 0 |
| transcription artefacts (':,' headings) | 4,118 | 69 |
| de-identification tokens (XXXX) | 3,423 | 0 |
| Open-i report without IMPRESSION | 34 | 6 |
| missing patient link | 8,954 | 0 |

## Cleaning log

- documents: rebuilt section headings in transcriptions: 4,118
- documents: marked de-identified words as [redacted]: 3,423
- documents: removed empty / very short: 158
- documents: merged duplicate transcriptions: 2,585
- documents: linked to patients by age+gender 1,058, by gender 1,879, at random (no gender/age in text) 3,274

## Documents by source / specialty

source
mtsamples    {'Surgery': 969, 'Radiology': 246, 'General Me...
openi                                      {'Radiology': 3878}