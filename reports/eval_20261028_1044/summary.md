# MedRAG evaluation

Run: 2026-10-28 13:49

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### documents questions (80)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.875 [0.80-0.94] | 0.809 [0.73-0.88] | 0.875 [0.80-0.94] | 0.825 [0.75-0.89] |          8.04 |

### easy questions (100)

| config                                                                              |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:------------------------------------------------------------------------------------|--------:|------:|-----------:|---------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |       1 |     1 |          1 |        1 |          1.68 |

### hard questions (78)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.987 [0.96-1.00] | 0.905 [0.85-0.95] | 0.983 [0.95-1.00] | 0.920 [0.88-0.96] |          2.58 |

### MRR by question type

| config                                                                              |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:------------------------------------------------------------------------------------|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |               1 |                0.975 |          0.562 |                          1 |                          0.7 |                     0.938 |                  0.815 |        0.875 |                1 |        1 |               1 |                1 |          1 |

### Recall on paraphrased questions, by whether the wording is in the expansion dictionary

| config                                                                              |   wording in dictionary=False |   wording in dictionary=True |
|:------------------------------------------------------------------------------------|------------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |                         0.926 |                            1 |

## Answers

| llm               | difficulty   | auto_correct      | fact_recall       | number_correct    | negative_correct   | abstain_correct   | cites_sources     |   Gen. time (s) |
|:------------------|:-------------|:------------------|:------------------|:------------------|:-------------------|:------------------|:------------------|----------------:|
| ollama:qwen2.5:3b | documents    | 0.500 [0.00-1.00] | 0.500 [0.00-1.00] | -                 | -                  | 0.750 [0.25-1.00] | 0.500 [0.00-1.00] |            52.3 |
| ollama:qwen2.5:3b | easy         | 0.625 [0.25-0.88] | 0.700 [0.30-1.00] | 0.500 [0.00-1.00] | -                  | 1.000             | 0.000             |            52.6 |
| ollama:qwen2.5:3b | hard         | 0.667 [0.33-1.00] | 0.917 [0.75-1.00] | 0.000             | 1.000              | 0.833 [0.50-1.00] | 0.167 [0.00-0.50] |            59.3 |
| ollama:qwen3:1.7b | documents    | 0.750 [0.25-1.00] | 0.750 [0.25-1.00] | -                 | -                  | 0.250 [0.00-0.75] | 0.500 [0.00-1.00] |            49.9 |
| ollama:qwen3:1.7b | easy         | 0.875 [0.62-1.00] | 1.000             | 0.500 [0.00-1.00] | -                  | 0.625 [0.25-0.88] | 0.625 [0.25-0.88] |            39.1 |
| ollama:qwen3:1.7b | hard         | 0.833 [0.50-1.00] | 1.000             | 0.000             | 1.000              | 0.333 [0.00-0.67] | 0.500 [0.17-0.83] |            43.4 |
| ollama:qwen3:4b   | documents    | 0.750 [0.25-1.00] | 0.750 [0.25-1.00] | -                 | -                  | 0.750 [0.25-1.00] | 0.750 [0.25-1.00] |           427.5 |
| ollama:qwen3:4b   | easy         | 0.875 [0.62-1.00] | 1.000             | 0.500 [0.00-1.00] | -                  | 0.875 [0.62-1.00] | 0.875 [0.62-1.00] |           384.8 |
| ollama:qwen3:4b   | hard         | 0.833 [0.50-1.00] | 1.000             | 0.000             | 1.000              | 0.833 [0.50-1.00] | 1.000             |           540.9 |

- auto_correct: pass/fail from the deterministic check that fits the question (exact number, all key facts, correct 'no', correct 'not found')
- judge_*: 1-5 scores from the judge model, which is a different model from the one answering

### auto_correct by question type

| llm               |   ambiguous_name |   count_cohort |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_count_finding |   hard_negative |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   not_found |   semantic |
|:------------------|-----------------:|---------------:|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|---------------------:|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|------------:|-----------:|
| ollama:qwen2.5:3b |                0 |              0 |               1 |                    1 |              0 |                          1 |                            0 |                    0 |               1 |                         1 |                      0 |            1 |                1 |        1 |               1 |                1 |           1 |          0 |
| ollama:qwen3:1.7b |                1 |              0 |               1 |                    1 |              1 |                          1 |                            0 |                    0 |               1 |                         1 |                      1 |            1 |                1 |        1 |               1 |                1 |           1 |          1 |
| ollama:qwen3:4b   |                1 |              0 |               1 |                    1 |              1 |                          1 |                            0 |                    0 |               1 |                         1 |                      1 |            1 |                1 |        1 |               1 |                1 |           1 |          1 |
