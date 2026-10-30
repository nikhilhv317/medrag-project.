# MedRAG evaluation

Run: 2026-10-30 09:41

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm               | difficulty   | auto_correct      | fact_recall       | number_correct   | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:------------------|:-------------|:------------------|:------------------|:-----------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| ollama:qwen3:1.7b | documents    | 0.750 [0.50-1.00] | 0.806 [0.58-1.00] | -                | -                  | 0.583 [0.33-0.83] | 0.583 [0.33-0.83] | -                   | -                    | -                        | -                         |             4.3 |
| ollama:qwen3:1.7b | easy         | 0.875 [0.75-1.00] | 0.833 [0.67-1.00] | 1.000            | -                  | 0.875 [0.75-1.00] | 0.250 [0.08-0.42] | 4.750 [4.25-5.00]   | 4.250 [3.50-5.00]    | 4.750 [4.25-5.00]        | 5.000                     |             4.3 |
| ollama:qwen3:1.7b | hard         | 0.688 [0.44-0.88] | 0.861 [0.67-1.00] | 0.000            | 1.000              | 0.625 [0.38-0.88] | 0.625 [0.38-0.81] | -                   | -                    | -                        | -                         |            38.1 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm               |   answers | correct (exact)   |   correct (judge) | faithfulness 1-5   | relevance 1-5     |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:------------------|----------:|:------------------|------------------:|:-------------------|:------------------|----------------------:|:------------------|:------------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| ollama:qwen3:1.7b |        52 | 0.788 [0.67-0.88] |                 1 | 4.250 [3.50-5.00]  | 4.750 [4.25-5.00] |                     1 | 0.286 [0.16-0.41] | 0.667 [0.33-1.00] | 0.696 [0.48-0.87]    | 0.156 [0.09-0.23]   |                       0 |          4.2 |         26.7 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm               |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| ollama:qwen3:1.7b |             0.33 |              1 |               1 |                 0.67 |           0.33 |                          1 |                            1 |                    0 |               1 |                         1 |                   0.67 |         0.67 |                1 |     0.67 |               1 |                1 |           1 |          1 |

Judge vs deterministic check agreement: 100% of 4 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.

**2 answers failed with errors**; see generation.csv.