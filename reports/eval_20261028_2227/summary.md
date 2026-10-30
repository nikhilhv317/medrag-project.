# MedRAG evaluation

Run: 2026-10-28 22:45

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### documents questions (80)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.950 [0.90-0.99] | 0.884 [0.83-0.94] | 0.950 [0.90-0.99] | 0.900 [0.85-0.95] |          8.26 |

### easy questions (100)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.910 [0.85-0.96] | 0.910 [0.85-0.96] | 0.910 [0.85-0.96] | 0.910 [0.85-0.96] |          1.81 |

### hard questions (78)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.987 [0.96-1.00] | 0.905 [0.85-0.95] | 0.983 [0.95-1.00] | 0.920 [0.88-0.96] |          2.88 |

### MRR by question type

| config                                                                              |   count_patient |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:------------------------------------------------------------------------------------|----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |               1 |                0.975 |          0.562 |                          1 |                            1 |                     0.938 |                  0.815 |        0.875 |                1 |        1 |            0.55 |                1 |          1 |

### Recall on paraphrased questions, by whether the wording is in the expansion dictionary

| config                                                                              |   wording in dictionary=False |   wording in dictionary=True |
|:------------------------------------------------------------------------------------|------------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |                         0.926 |                            1 |
