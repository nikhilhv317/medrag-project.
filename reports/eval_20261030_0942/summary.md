# MedRAG evaluation

Run: 2026-10-30 09:46

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm               | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     |   Gen. time (s) |
|:------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|----------------:|
| ollama:qwen2.5:3b | documents    | 0.333 [0.08-0.58] | 0.444 [0.22-0.69] | -                 | -                  | 0.917 [0.75-1.00] | 0.417 [0.17-0.75] |             5   |
| ollama:qwen2.5:3b | easy         | 0.958 [0.88-1.00] | 0.933 [0.80-1.00] | 1.000             | -                  | 1.000             | 0.250 [0.08-0.42] |            63.5 |
| ollama:qwen2.5:3b | hard         | 0.833 [0.67-1.00] | 0.944 [0.83-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.778 [0.56-0.94] | 0.333 [0.11-0.56] |             4.3 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm               |   answers | correct (exact)   |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:------------------|----------:|:------------------|----------------------:|:------------------|:------------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| ollama:qwen2.5:3b |        54 | 0.778 [0.67-0.89] |                     1 | 0.098 [0.02-0.18] | 0.778 [0.56-1.00] | 0.882 [0.71-1.00]    | 0.033 [0.00-0.08]   |                       0 |          3.9 |          9.2 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm               |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| ollama:qwen2.5:3b |                1 |              1 |               1 |                 0.67 |              0 |                       0.67 |                            0 |                 0.33 |               1 |                         1 |                   0.67 |            1 |                1 |        1 |               1 |                1 |           1 |       0.67 |
