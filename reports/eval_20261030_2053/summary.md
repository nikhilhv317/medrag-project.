# MedRAG evaluation

Run: 2026-10-30 21:00

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm               | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| ollama:qwen2.5:3b | documents    | 0.333 [0.08-0.58] | 0.444 [0.22-0.69] | -                 | -                  | 0.917 [0.75-1.00] | 0.417 [0.17-0.75] | 2.833 [1.83-3.92]   | 4.583 [3.83-5.00]    | 3.167 [2.17-4.08]        | 5.000                     |             5   |
| ollama:qwen2.5:3b | easy         | 0.958 [0.88-1.00] | 0.933 [0.80-1.00] | 1.000             | -                  | 1.000             | 0.250 [0.08-0.42] | 4.348 [3.70-4.83]   | 4.522 [4.00-5.00]    | 4.609 [4.22-4.96]        | 4.478 [3.96-5.00]         |            63.5 |
| ollama:qwen2.5:3b | hard         | 0.833 [0.67-1.00] | 0.944 [0.83-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.778 [0.56-0.94] | 0.333 [0.11-0.56] | 3.278 [2.39-4.17]   | 4.167 [3.55-4.72]    | 3.611 [3.00-4.22]        | 4.833 [4.50-5.00]         |             4.3 |
| ollama:qwen3:1.7b | documents    | 0.833 [0.58-1.00] | 0.889 [0.72-1.00] | -                 | -                  | 0.750 [0.50-1.00] | 0.500 [0.25-0.75] | 4.000 [3.25-4.67]   | 4.250 [3.58-4.83]    | 4.167 [3.50-4.75]        | 5.000                     |             4.5 |
| ollama:qwen3:1.7b | easy         | 0.917 [0.79-1.00] | 0.900 [0.77-1.00] | 1.000             | -                  | 0.833 [0.67-0.96] | 0.458 [0.25-0.67] | 5.000               | 4.958 [4.88-5.00]    | 4.875 [4.71-5.00]        | 4.500 [4.00-5.00]         |             3.8 |
| ollama:qwen3:1.7b | hard         | 0.833 [0.67-1.00] | 1.000             | 0.000             | 1.000              | 0.556 [0.33-0.78] | 0.500 [0.28-0.72] | 3.222 [2.44-4.11]   | 4.111 [3.50-4.67]    | 3.389 [2.72-4.06]        | 4.833 [4.50-5.00]         |             4.3 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm               |   answers | correct (exact)   | correct (judge)   | faithfulness 1-5   | relevance 1-5     |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:------------------|----------:|:------------------|:------------------|:-------------------|:------------------|----------------------:|:------------------|:------------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| ollama:qwen3:1.7b |        54 | 0.870 [0.78-0.94] | 0.778 [0.65-0.89] | 4.519 [4.20-4.78]  | 4.222 [3.89-4.56] |                     1 | 0.294 [0.18-0.41] | 0.667 [0.33-1.00] | 0.654 [0.50-0.81]    | 0.224 [0.13-0.33]   |                       0 |          3.8 |          7   |
| ollama:qwen2.5:3b |        54 | 0.778 [0.67-0.89] | 0.660 [0.53-0.77] | 4.415 [4.06-4.74]  | 3.943 [3.57-4.32] |                     1 | 0.098 [0.02-0.18] | 0.778 [0.56-1.00] | 0.882 [0.71-1.00]    | 0.033 [0.00-0.08]   |                       0 |          3.9 |          9.2 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm               |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| ollama:qwen2.5:3b |             1    |              1 |               1 |                 0.67 |           0    |                       0.67 |                            0 |                 0.33 |               1 |                         1 |                   0.67 |            1 |                1 |     1    |               1 |                1 |           1 |       0.67 |
| ollama:qwen3:1.7b |             0.67 |              1 |               1 |                 0.67 |           0.67 |                       1    |                            1 |                 0    |               1 |                         1 |                   1    |            1 |                1 |     0.67 |               1 |                1 |           1 |       1    |

Judge vs deterministic check agreement: 80% of 107 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.
