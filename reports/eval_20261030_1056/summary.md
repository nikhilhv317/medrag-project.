# MedRAG evaluation

Run: 2026-10-30 11:17

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm                          | difficulty   | auto_correct      | fact_recall       | abstain_correct   | cites_sources     |   Gen. time (s) |
|:-----------------------------|:-------------|:------------------|:------------------|:------------------|:------------------|----------------:|
| gemini:gemini-3.5-flash-lite | documents    | 0.933 [0.87-0.98] | 0.933 [0.87-0.98] | 0.950 [0.88-1.00] | 0.967 [0.92-1.00] |               2 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm                          |   answers | correct (exact)   | abstain when needed   | false abstain     | exact numbers   | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:-----------------------------|----------:|:------------------|:----------------------|:------------------|:----------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| gemini:gemini-3.5-flash-lite |        60 | 0.933 [0.87-0.98] | -                     | 0.050 [0.00-0.12] | -               | 0.962 [0.92-0.99]    | 0.880 [0.83-0.93]   |                       0 |          1.7 |          4.3 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm                          |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |
|:-----------------------------|---------------------:|---------------:|---------------------------:|-----------------------------:|
| gemini:gemini-3.5-flash-lite |                    1 |            0.8 |                          1 |                         0.93 |
