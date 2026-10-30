# MedRAG evaluation

Run: 2026-10-30 21:10

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Answers

| llm                           | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:------------------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| gemini:gemini-3-flash-preview | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.875 [0.75-1.00] | 5.000               | 5.000                | 4.870 [4.70-5.00]        | 4.478 [3.96-5.00]         |             7.5 |
| gemini:gemini-3.1-flash-lite  | documents    | 0.917 [0.75-1.00] | 0.972 [0.92-1.00] | -                 | -                  | 1.000             | 0.833 [0.58-1.00] | 4.917 [4.75-5.00]   | 5.000                | 4.917 [4.75-5.00]        | 5.000                     |             1.3 |
| gemini:gemini-3.1-flash-lite  | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.750 [0.58-0.92] | 4.955 [4.86-5.00]   | 4.955 [4.86-5.00]    | 4.909 [4.77-5.00]        | 4.455 [3.91-5.00]         |            13.1 |
| gemini:gemini-3.1-flash-lite  | hard         | 0.778 [0.61-0.94] | 0.833 [0.58-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.667 [0.44-0.89] | 0.778 [0.56-0.94] | 4.167 [3.44-4.78]   | 4.778 [4.50-5.00]    | 4.389 [3.89-4.83]        | 4.667 [4.17-5.00]         |             3.5 |
| gemini:gemini-3.5-flash       | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.708 [0.54-0.88] | 5.000               | 5.000                | 4.905 [4.76-5.00]        | 4.429 [3.86-5.00]         |             9.7 |
| gemini:gemini-3.5-flash       | hard         | 0.800 [0.60-1.00] | 0.963 [0.89-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.800 [0.60-1.00] | 0.733 [0.53-0.93] | 4.333 [3.53-5.00]   | 4.533 [3.80-5.00]    | 4.467 [3.87-4.93]        | 4.867 [4.60-5.00]         |             4.2 |
| gemini:gemini-3.5-flash-lite  | documents    | 0.833 [0.58-1.00] | 0.889 [0.72-1.00] | -                 | -                  | 0.917 [0.75-1.00] | 0.917 [0.75-1.00] | 4.667 [4.00-5.00]   | 4.833 [4.58-5.00]    | 4.667 [4.00-5.00]        | 5.000                     |             6.6 |
| gemini:gemini-3.5-flash-lite  | easy         | 1.000             | 1.000             | 1.000             | -                  | 1.000             | 0.667 [0.50-0.83] | 5.000               | 5.000                | 4.909 [4.77-5.00]        | 4.455 [3.91-5.00]         |             2.5 |
| gemini:gemini-3.5-flash-lite  | hard         | 0.833 [0.67-1.00] | 0.917 [0.75-1.00] | 0.333 [0.00-1.00] | 1.000              | 0.833 [0.67-1.00] | 0.722 [0.50-0.89] | 4.333 [3.67-5.00]   | 4.722 [4.33-5.00]    | 4.500 [4.00-5.00]        | 4.778 [4.33-5.00]         |             5.8 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### Answer quality, one metric per column

| llm                           |   answers | correct (exact)   | correct (judge)   | faithfulness 1-5   | relevance 1-5     |   abstain when needed | false abstain     | exact numbers     | citation precision   | citation coverage   |   invalid citation rate |   gen. s p50 |   gen. s p95 |
|:------------------------------|----------:|:------------------|:------------------|:-------------------|:------------------|----------------------:|:------------------|:------------------|:---------------------|:--------------------|------------------------:|-------------:|-------------:|
| gemini:gemini-3.5-flash       |        39 | 0.923 [0.85-1.00] | 0.917 [0.81-1.00] | 4.806 [4.47-5.00]  | 4.722 [4.44-4.94] |                     1 | 0.083 [0.00-0.19] | 0.778 [0.56-1.00] | 0.994 [0.98-1.00]    | 0.659 [0.53-0.78]   |                       0 |          4.5 |         22.9 |
| gemini:gemini-3.5-flash-lite  |        54 | 0.907 [0.81-0.98] | 0.923 [0.85-0.98] | 4.865 [4.73-4.96]  | 4.712 [4.46-4.92] |                     1 | 0.078 [0.02-0.16] | 0.778 [0.56-1.00] | 0.930 [0.86-0.98]    | 0.689 [0.58-0.78]   |                       0 |          3.8 |          9   |
| gemini:gemini-3.1-flash-lite  |        54 | 0.907 [0.83-0.98] | 0.923 [0.85-0.98] | 4.904 [4.79-4.98]  | 4.731 [4.52-4.90] |                     1 | 0.118 [0.04-0.22] | 0.778 [0.56-1.00] | 0.896 [0.81-0.97]    | 0.768 [0.67-0.86]   |                       0 |          1.3 |         32.3 |
| gemini:gemini-3-flash-preview |        24 | 1.000             | 1.000             | 5.000              | 4.870 [4.70-5.00] |                     1 | 0.000             | 1.000             | 0.890 [0.80-0.97]    | 0.640 [0.51-0.75]   |                       0 |          3   |         45   |

- correct (exact): deterministic check; correct (judge): judge correctness >= 4
- abstain when needed: share of unanswerable questions answered 'not found'; false abstain: share of answerable ones
- exact numbers: count questions only; citations: cited sentences supported by the cited sources (verify_citations)

### auto_correct by question type

| llm                           |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| gemini:gemini-3-flash-preview |                1 |              1 |               1 |                  nan |         nan    |                     nan    |                          nan |               nan    |             nan |                       nan |                 nan    |       nan    |              nan |        1 |               1 |                1 |           1 |          1 |
| gemini:gemini-3.1-flash-lite  |                1 |              1 |               1 |                    1 |           1    |                       0.67 |                            1 |                 0.33 |               1 |                         1 |                   0.33 |         1    |                1 |        1 |               1 |                1 |           1 |          1 |
| gemini:gemini-3.5-flash       |                1 |              1 |               1 |                  nan |         nan    |                     nan    |                          nan |                 0.33 |               1 |                         1 |                   0.67 |         1    |              nan |        1 |               1 |                1 |           1 |          1 |
| gemini:gemini-3.5-flash-lite  |                1 |              1 |               1 |                    1 |           0.67 |                       0.67 |                            1 |                 0.33 |               1 |                         1 |                   1    |         0.67 |                1 |        1 |               1 |                1 |           1 |          1 |

Judge vs deterministic check agreement: 99% of 163 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.

**45 answers failed with errors**; see generation.csv.