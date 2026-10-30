# MedRAG evaluation

Run: 2026-10-29 11:48

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm                           | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:------------------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| gemini:gemini-3-flash-preview | easy         | 1.000             | -                 | -                 | -                  | 1.000             | 0.000             | -                   | -                    | -                        | -                         |             0   |
| gemini:gemini-3.1-flash-lite  | easy         | 1.000             | -                 | -                 | -                  | 1.000             | 0.000             | -                   | -                    | -                        | -                         |             0   |
| gemini:gemini-3.5-flash       | easy         | 1.000             | 1.000             | -                 | -                  | 1.000             | 0.727 [0.45-1.00] | 5.000               | 5.000                | 5.000                    | 5.000                     |             5.5 |
| gemini:gemini-3.5-flash-lite  | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.667 [0.50-0.83] | 5.000               | 5.000                | 5.000                    | 5.000                     |             2.2 |
| gemini:gemini-3.5-flash-lite  | hard         | 0.750 [0.50-0.94] | 0.800 [0.60-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.875 [0.69-1.00] | 0.812 [0.62-1.00] | 5.000               | 5.000                | 5.000                    | 5.000                     |             2.4 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm                           |   answers | correct (exact)   |   correct (judge) |   faithfulness 1-5 |   relevance 1-5 |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   | invalid citation rate   |   gen. s p50 |   gen. s p95 |
|:------------------------------|----------:|:------------------|------------------:|-------------------:|----------------:|----------------------:|:------------------|:------------------|:---------------------|:--------------------|:------------------------|-------------:|-------------:|
| gemini:gemini-3.5-flash       |        11 | 1.000             |                 1 |                  5 |               5 |                     1 | 0.000             | -                 | 0.979 [0.94-1.00]    | 0.629 [0.38-0.84]   | 0.000                   |          2.9 |         20.3 |
| gemini:gemini-3.5-flash-lite  |        40 | 0.900 [0.80-0.97] |                 1 |                  5 |               5 |                     1 | 0.054 [0.00-0.14] | 0.778 [0.56-1.00] | 0.887 [0.77-0.98]    | 0.693 [0.57-0.81]   | 0.000                   |          1.5 |          6.5 |
| gemini:gemini-3.1-flash-lite  |         3 | 1.000             |               nan |                nan |             nan |                     1 | -                 | -                 | -                    | 0.000               | -                       |          0   |          0   |
| gemini:gemini-3-flash-preview |         3 | 1.000             |               nan |                nan |             nan |                     1 | -                 | -                 | -                    | 0.000               | -                       |          0   |          0   |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm                           |   ambiguous_name |   count_cohort |   count_patient |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------------------|-----------------:|---------------:|----------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| gemini:gemini-3-flash-preview |              nan |            nan |             nan |               nan    |             nan |                       nan |                 nan    |       nan    |              nan |      nan |             nan |              nan |           1 |        nan |
| gemini:gemini-3.1-flash-lite  |              nan |            nan |             nan |               nan    |             nan |                       nan |                 nan    |       nan    |              nan |      nan |             nan |              nan |           1 |        nan |
| gemini:gemini-3.5-flash       |              nan |            nan |             nan |               nan    |             nan |                       nan |                 nan    |       nan    |              nan |        1 |               1 |                1 |           1 |        nan |
| gemini:gemini-3.5-flash-lite  |                1 |              1 |               1 |                 0.33 |               1 |                         1 |                   0.67 |         0.67 |                1 |        1 |               1 |                1 |           1 |          1 |

Judge vs deterministic check agreement: 100% of 10 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.

**159 answers failed with errors**; see generation.csv.