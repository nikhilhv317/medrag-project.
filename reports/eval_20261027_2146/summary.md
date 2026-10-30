# MedRAG evaluation

Run: 2026-10-27 23:35

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### documents questions (40)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.900 [0.80-0.97] | 0.808 [0.70-0.91] | 0.900 [0.80-0.97] | 0.831 [0.72-0.93] |         10.12 |

### easy questions (100)

| config                                                                              |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:------------------------------------------------------------------------------------|--------:|------:|-----------:|---------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |       1 |     1 |          1 |        1 |          1.18 |

### hard questions (78)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.987 [0.96-1.00] | 0.905 [0.85-0.95] | 0.983 [0.95-1.00] | 0.920 [0.88-0.96] |          2.22 |

### MRR by question type

| config                                                                              |   count_patient |   doc_patient_lookup |   doc_semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:------------------------------------------------------------------------------------|----------------:|---------------------:|---------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |               1 |                0.975 |          0.642 |                     0.938 |                  0.815 |        0.875 |                1 |        1 |               1 |                1 |          1 |

### Recall on paraphrased questions, by whether the wording is in the expansion dictionary

| config                                                                              |   wording in dictionary=False |   wording in dictionary=True |
|:------------------------------------------------------------------------------------|------------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |                         0.926 |                            1 |

## Answers

| llm                     | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     | judge_correctness   | judge_faithfulness   | judge_answer_relevance   | judge_context_relevance   |   Gen. time (s) |
|:------------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|:--------------------|:---------------------|:-------------------------|:--------------------------|----------------:|
| gemini:gemini-3.8-flash | easy         | 1.000             | 1.000             | -                 | -                  | 1.000             | 0.667 [0.00-1.00] | -                   | -                    | -                        | -                         |           191.3 |
| ollama:qwen2.5:3b       | documents    | 0.500 [0.00-1.00] | 0.500 [0.00-1.00] | -                 | -                  | 1.000             | 1.000             | 3.000 [1.00-5.00]   | 3.000 [1.00-5.00]    | 5.000                    | 5.000                     |            45.3 |
| ollama:qwen2.5:3b       | easy         | 0.750 [0.50-1.00] | 0.900 [0.70-1.00] | 0.500 [0.00-1.00] | -                  | 1.000             | 0.125 [0.00-0.38] | 3.500 [2.00-5.00]   | 3.500 [2.00-5.00]    | 4.000 [3.00-5.00]        | 5.000                     |            45.3 |
| ollama:qwen2.5:3b       | hard         | 0.667 [0.33-1.00] | 0.917 [0.75-1.00] | 0.000             | 1.000              | 0.833 [0.50-1.00] | 0.167 [0.00-0.50] | 1.000               | 1.000                | 5.000                    | 2.000                     |            50.3 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### auto_correct by question type

| llm                     |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| gemini:gemini-3.8-flash |              nan |            nan |             nan |                  nan |            nan |                  nan |             nan |                       nan |                    nan |          nan |              nan |        1 |               1 |              nan |           1 |        nan |
| ollama:qwen2.5:3b       |                0 |              0 |               1 |                    1 |              0 |                    0 |               1 |                         1 |                      0 |            1 |                1 |        1 |               1 |                1 |           1 |          1 |

Judge vs deterministic check agreement: 100% of 5 answers (judge correctness >= 4 counted as pass). Low agreement means one of the two needs review.

**13 answers failed with errors**; see generation.csv.