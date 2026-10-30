# MedRAG evaluation

Run: 2026-10-30 22:26

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm                                           | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:----------------------------------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| nvidia:nvidia/nemotron-3.5-lightning-30b-a3b  | documents    | 0.667 [0.42-0.92] | 0.722 [0.47-0.92] | -                 | -                  | 1.000             | 0.917 [0.75-1.00] | 4.583 [3.92-5.00]   | 4.750 [4.25-5.00]    | 4.750 [4.25-5.00]        | 5.000                     |             2.6 |
| nvidia:nvidia/nemotron-3.5-lightning-30b-a3b  | easy         | 0.875 [0.75-1.00] | 0.800 [0.60-1.00] | 1.000             | -                  | 1.000             | 0.708 [0.54-0.88] | 4.750 [4.38-5.00]   | 4.792 [4.42-5.00]    | 4.833 [4.54-5.00]        | 4.500 [4.00-5.00]         |             1.6 |
| nvidia:nvidia/nemotron-3.5-lightning-30b-a3b  | hard         | 0.722 [0.50-0.89] | 0.833 [0.58-1.00] | 0.333 [0.00-1.00] | 0.667 [0.00-1.00]  | 1.000             | 0.889 [0.72-1.00] | 4.056 [3.39-4.78]   | 4.333 [3.72-4.83]    | 4.333 [3.83-4.83]        | 4.889 [4.67-5.00]         |             1.9 |
| nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b | documents    | 0.833 [0.58-1.00] | 0.917 [0.78-1.00] | -                 | -                  | 1.000             | 1.000             | 4.917 [4.75-5.00]   | 4.833 [4.58-5.00]    | 5.000                    | 5.000                     |             1.3 |
| nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.750 [0.58-0.92] | 5.000               | 4.958 [4.88-5.00]    | 4.917 [4.79-5.00]        | 4.500 [4.00-5.00]         |             2.4 |
| nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b | hard         | 0.833 [0.67-1.00] | 0.917 [0.75-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.944 [0.83-1.00] | 0.889 [0.72-1.00] | 4.278 [3.61-4.89]   | 4.667 [4.28-4.94]    | 4.500 [4.00-5.00]        | 4.889 [4.67-5.00]         |             2.5 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm                                           |   answers | correct (exact)   | correct (judge)   | faithfulness 1-5   | relevance 1-5     |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:----------------------------------------------|----------:|:------------------|:------------------|:-------------------|:------------------|----------------------:|:------------------|:------------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b |        54 | 0.907 [0.81-0.98] | 0.944 [0.87-1.00] | 4.833 [4.69-4.94]  | 4.796 [4.57-4.96] |                     1 | 0.020 [0.00-0.06] | 0.778 [0.56-1.00] | 0.978 [0.93-1.00]    | 0.559 [0.44-0.67]   |                       0 |          0.9 |         13   |
| nvidia:nvidia/nemotron-3.5-lightning-30b-a3b  |        54 | 0.778 [0.67-0.89] | 0.889 [0.80-0.96] | 4.630 [4.35-4.89]  | 4.648 [4.39-4.89] |                     1 | 0.000             | 0.778 [0.56-1.00] | 0.972 [0.91-1.00]    | 0.158 [0.09-0.24]   |                       0 |          1.2 |          5.6 |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm                                           |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:----------------------------------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| nvidia:nvidia/nemotron-3.5-lightning-30b-a3b  |                1 |              1 |               1 |                    1 |           0.67 |                       0.67 |                         0.33 |                 0.33 |            0.67 |                         1 |                   0.33 |         1    |                1 |        1 |               1 |                1 |           1 |          0 |
| nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b |                1 |              1 |               1 |                    1 |           1    |                       0.33 |                         1    |                 0.33 |            1    |                         1 |                   1    |         0.67 |                1 |        1 |               1 |                1 |           1 |          1 |

Judge vs deterministic check agreement: 91% of 108 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.
