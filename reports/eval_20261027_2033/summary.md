# MedRAG evaluation

Run: 2026-10-27 21:17

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### documents questions (40)

| config                                                                                         | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:-----------------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2, replace) | 0.950 [0.88-1.00] | 0.851 [0.75-0.94] | 0.950 [0.88-1.00] | 0.875 [0.78-0.95] |          1.43 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                            | 0.925 [0.82-1.00] | 0.837 [0.73-0.93] | 0.925 [0.82-1.00] | 0.859 [0.76-0.94] |          0.06 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder)            | 0.900 [0.80-0.97] | 0.808 [0.70-0.91] | 0.900 [0.80-0.97] | 0.831 [0.72-0.93] |          7    |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2)          | 0.900 [0.80-0.97] | 0.797 [0.68-0.90] | 0.900 [0.80-0.97] | 0.822 [0.71-0.91] |          1.68 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion               | 0.900 [0.80-0.97] | 0.797 [0.68-0.90] | 0.900 [0.80-0.97] | 0.822 [0.71-0.91] |          1.43 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder, replace)   | 0.950 [0.88-1.00] | 0.793 [0.69-0.89] | 0.950 [0.88-1.00] | 0.832 [0.74-0.91] |          7.02 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                          | 0.875 [0.78-0.97] | 0.762 [0.64-0.87] | 0.875 [0.78-0.97] | 0.790 [0.68-0.89] |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                           | 0.750 [0.62-0.88] | 0.621 [0.48-0.76] | 0.750 [0.62-0.88] | 0.652 [0.51-0.79] |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters                       | 0.875 [0.78-0.97] | 0.507 [0.41-0.62] | 0.875 [0.78-0.97] | 0.599 [0.51-0.69] |          3.95 |

### easy questions (100)

| config                                                                                         | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:-----------------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                            | 1.000             | 1.000             | 1.000             | 1.000             |          0.04 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                          | 1.000             | 1.000             | 1.000             | 1.000             |          0.09 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder)            | 1.000             | 1.000             | 1.000             | 1.000             |          1.45 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder, replace)   | 1.000             | 1.000             | 1.000             | 1.000             |          1.42 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2)          | 1.000             | 1.000             | 1.000             | 1.000             |          0.41 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2, replace) | 1.000             | 1.000             | 1.000             | 1.000             |          0.33 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                           | 1.000             | 0.995 [0.98-1.00] | 1.000             | 0.996 [0.99-1.00] |          0.09 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion               | 1.000             | 0.995 [0.98-1.00] | 1.000             | 0.996 [0.99-1.00] |          0.32 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters                       | 0.710 [0.62-0.79] | 0.495 [0.41-0.57] | 0.710 [0.62-0.79] | 0.549 [0.47-0.63] |          3.7  |

### hard questions (78)

| config                                                                                         | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:-----------------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder, replace)   | 0.974 [0.94-1.00] | 0.915 [0.86-0.96] | 0.966 [0.92-1.00] | 0.923 [0.87-0.96] |          2.46 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                           | 0.962 [0.91-1.00] | 0.913 [0.85-0.96] | 0.962 [0.91-1.00] | 0.925 [0.87-0.97] |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder)            | 0.987 [0.96-1.00] | 0.905 [0.85-0.95] | 0.983 [0.95-1.00] | 0.920 [0.88-0.96] |          2.48 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2)          | 0.974 [0.94-1.00] | 0.885 [0.82-0.94] | 0.970 [0.93-1.00] | 0.902 [0.85-0.95] |          0.63 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                          | 1.000             | 0.875 [0.81-0.93] | 0.996 [0.99-1.00] | 0.900 [0.85-0.94] |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2, replace) | 0.962 [0.91-1.00] | 0.872 [0.81-0.93] | 0.953 [0.91-1.00] | 0.893 [0.84-0.94] |          0.54 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                            | 0.936 [0.87-0.99] | 0.865 [0.80-0.93] | 0.915 [0.85-0.97] | 0.878 [0.81-0.94] |          0.05 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion               | 0.962 [0.92-1.00] | 0.793 [0.72-0.86] | 0.953 [0.91-0.99] | 0.828 [0.77-0.88] |          0.52 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters                       | 0.756 [0.65-0.85] | 0.509 [0.42-0.60] | 0.709 [0.61-0.80] | 0.553 [0.46-0.64] |          4.74 |

### MRR by question type

| config                                                                                         |   count_patient |   doc_patient_lookup |   doc_semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:-----------------------------------------------------------------------------------------------|----------------:|---------------------:|---------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                            |            1    |                0.95  |          0.724 |                     0.925 |                  0.572 |        0.975 |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                           |            1    |                0.975 |          0.266 |                     0.975 |                  0.81  |        0.875 |            1     |    1     |           1     |            1     |      0.975 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                          |            1    |                0.975 |          0.549 |                     0.938 |                  0.701 |        0.875 |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder)            |            1    |                0.975 |          0.642 |                     0.938 |                  0.815 |        0.875 |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder, replace)   |            1    |                0.95  |          0.637 |                     0.942 |                  0.85  |        0.875 |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2)          |            1    |                0.975 |          0.618 |                     0.933 |                  0.745 |        0.875 |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2, replace) |            1    |                1     |          0.702 |                     0.875 |                  0.727 |        0.9   |            1     |    1     |           1     |            1     |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters                       |            0.95 |                0.42  |          0.594 |                     0.85  |                  0.096 |        0.75  |            0.324 |    0.006 |           0.817 |            0.485 |      0.218 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion               |            1    |                0.975 |          0.618 |                     0.706 |                  0.586 |        0.9   |            1     |    1     |           1     |            1     |      0.975 |

### Recall on paraphrased questions, by whether the wording is in the expansion dictionary

| config                                                                                         |   wording in dictionary=False |   wording in dictionary=True |
|:-----------------------------------------------------------------------------------------------|------------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                            |                         0.63  |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                           |                         0.833 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                          |                         0.981 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder)            |                         0.926 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder, replace)   |                         0.852 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2)          |                         0.87  |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2, replace) |                         0.796 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters                       |                         0.352 |                        0.833 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion               |                         0.87  |                        0.968 |
