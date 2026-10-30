# MedRAG evaluation

Run: 2026-10-27 20:18

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### easy questions (100)

| config                                                                                | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:--------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                   | 1.000             | 1.000             | 1.000             | 1.000             |          0.05 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                 | 1.000             | 1.000             | 1.000             | 1.000             |          0.09 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (bge-reranker-base)      | 1.000             | 1.000             | 1.000             | 1.000             |          1.69 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion      | 1.000             | 1.000             | 1.000             | 1.000             |          0.35 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2) | 1.000             | 1.000             | 1.000             | 1.000             |          0.31 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                  | 1.000             | 0.995 [0.98-1.00] | 1.000             | 0.996 [0.99-1.00] |          0.08 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters              | 0.730 [0.64-0.81] | 0.643 [0.56-0.73] | 0.730 [0.64-0.81] | 0.666 [0.58-0.75] |          3.28 |

### hard questions (78)

| config                                                                                | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:--------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                  | 0.962 [0.91-1.00] | 0.913 [0.85-0.96] | 0.962 [0.91-1.00] | 0.925 [0.87-0.97] |          0.13 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                 | 1.000             | 0.876 [0.81-0.93] | 0.996 [0.99-1.00] | 0.901 [0.86-0.94] |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2) | 0.974 [0.94-1.00] | 0.874 [0.81-0.93] | 0.966 [0.92-1.00] | 0.897 [0.85-0.95] |          0.51 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                   | 0.949 [0.90-0.99] | 0.873 [0.80-0.94] | 0.927 [0.87-0.98] | 0.887 [0.82-0.95] |          0.06 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (bge-reranker-base)      | 0.949 [0.90-0.99] | 0.845 [0.78-0.91] | 0.927 [0.88-0.98] | 0.863 [0.80-0.92] |          3.28 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion      | 0.962 [0.92-1.00] | 0.817 [0.75-0.88] | 0.944 [0.90-0.99] | 0.847 [0.78-0.91] |          0.6  |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters              | 0.769 [0.67-0.86] | 0.587 [0.50-0.68] | 0.750 [0.65-0.84] | 0.627 [0.54-0.71] |          2.7  |

### MRR by question type

| config                                                                                |   count_patient |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:--------------------------------------------------------------------------------------|----------------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                   |               1 |                     0.957 |                  0.572 |        0.975 |            1     |        1 |            1    |             1    |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                  |               1 |                     0.975 |                  0.81  |        0.875 |            1     |        1 |            1    |             1    |      0.975 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                 |               1 |                     0.942 |                  0.701 |        0.875 |            1     |        1 |            1    |             1    |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (bge-reranker-base)      |               1 |                     0.888 |                  0.558 |        0.95  |            1     |        1 |            1    |             1    |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2) |               1 |                     0.882 |                  0.727 |        0.9   |            1     |        1 |            1    |             1    |      1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters              |               1 |                     0.721 |                  0.039 |        0.817 |            0.792 |        0 |            0.85 |             0.85 |      0.517 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion      |               1 |                     0.765 |                  0.595 |        0.925 |            1     |        1 |            1    |             1    |      1     |

### Recall on paraphrased questions, by whether the wording is in the expansion dictionary

| config                                                                                |   wording in dictionary=False |   wording in dictionary=True |
|:--------------------------------------------------------------------------------------|------------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                                   |                         0.685 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                                  |                         0.833 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                                 |                         0.981 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (bge-reranker-base)      |                         0.685 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (ms-marco-MiniLM-L-6-v2) |                         0.852 |                        1     |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no filters              |                         0.333 |                        0.821 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank, no query expansion      |                         0.852 |                        0.96  |
