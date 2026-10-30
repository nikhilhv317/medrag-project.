# MedRAG evaluation

Run: 2026-10-30 10:56

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm                          | difficulty   | auto_correct      | fact_recall       | abstain_correct   | cites_sources     |   Gen. time (s) |
|:-----------------------------|:-------------|:------------------|:------------------|:------------------|:------------------|----------------:|
| gemini:gemini-3.5-flash-lite | documents    | 0.833 [0.73-0.93] | 0.894 [0.82-0.96] | 0.950 [0.88-1.00] | 0.917 [0.83-0.98] |             1.6 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm                          |   answers | correct (exact)   | abstain when needed   | false abstain     | exact numbers   | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:-----------------------------|----------:|:------------------|:----------------------|:------------------|:----------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| gemini:gemini-3.5-flash-lite |        60 | 0.833 [0.73-0.93] | -                     | 0.050 [0.00-0.12] | -               | 0.956 [0.91-0.99]    | 0.905 [0.85-0.95]   |                       0 |          1.4 |          2.9 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm                          |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |
|:-----------------------------|---------------------:|---------------:|---------------------------:|-----------------------------:|
| gemini:gemini-3.5-flash-lite |                 0.93 |            0.8 |                       0.67 |                         0.93 |
