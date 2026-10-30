# Embedding model benchmark

Compare rows with each other only (see medrag/eval/bench.py).

## documents (80 questions)

| config                                                                 | MRR               | Recall@8          | nDCG@8            | Hit@8             |   Latency (s) |
|:-----------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| medcpt:ncbi/MedCPT | dense                                             | 0.727 [0.64-0.82] | 0.787 [0.69-0.86] | 0.742 [0.65-0.83] | 0.787 [0.69-0.86] |          0.02 |
| medcpt:ncbi/MedCPT | hybrid+rerank                                     | 0.881 [0.81-0.94] | 0.925 [0.86-0.97] | 0.892 [0.82-0.95] | 0.925 [0.86-0.97] |          0.23 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | dense                    | 0.812 [0.73-0.88] | 0.887 [0.82-0.95] | 0.831 [0.75-0.90] | 0.887 [0.82-0.95] |          0.03 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | hybrid+rerank            | 0.888 [0.83-0.94] | 0.950 [0.90-0.99] | 0.903 [0.85-0.95] | 0.950 [0.90-0.99] |          0.23 |
| sentence-transformers:intfloat/e5-base-v2 | dense                      | 0.798 [0.72-0.87] | 0.863 [0.79-0.93] | 0.814 [0.74-0.88] | 0.863 [0.79-0.93] |          0.02 |
| sentence-transformers:intfloat/e5-base-v2 | hybrid+rerank              | 0.877 [0.81-0.93] | 0.963 [0.93-1.00] | 0.898 [0.84-0.94] | 0.963 [0.93-1.00] |          0.23 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | dense         | 0.735 [0.64-0.82] | 0.787 [0.70-0.88] | 0.748 [0.65-0.84] | 0.787 [0.70-0.88] |          0.02 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | hybrid+rerank | 0.834 [0.76-0.89] | 0.963 [0.93-1.00] | 0.865 [0.80-0.92] | 0.963 [0.93-1.00] |          0.24 |
| ollama:nomic-embed-text | dense                                        | 0.811 [0.73-0.88] | 0.887 [0.82-0.95] | 0.830 [0.75-0.90] | 0.887 [0.82-0.95] |          2.25 |
| ollama:nomic-embed-text | hybrid+rerank                                | 0.895 [0.83-0.95] | 0.963 [0.93-1.00] | 0.912 [0.86-0.95] | 0.963 [0.93-1.00] |          0.31 |

## easy (100 questions)

| config                                                                 |   MRR |   Recall@8 |   nDCG@8 |   Hit@8 |   Latency (s) |
|:-----------------------------------------------------------------------|------:|-----------:|---------:|--------:|--------------:|
| medcpt:ncbi/MedCPT | dense                                             |     1 |          1 |        1 |       1 |          0.02 |
| medcpt:ncbi/MedCPT | hybrid+rerank                                     |     1 |          1 |        1 |       1 |          0.06 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | dense                    |     1 |          1 |        1 |       1 |          0.02 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | hybrid+rerank            |     1 |          1 |        1 |       1 |          0.04 |
| sentence-transformers:intfloat/e5-base-v2 | dense                      |     1 |          1 |        1 |       1 |          0.02 |
| sentence-transformers:intfloat/e5-base-v2 | hybrid+rerank              |     1 |          1 |        1 |       1 |          0.04 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | dense         |     1 |          1 |        1 |       1 |          0.02 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | hybrid+rerank |     1 |          1 |        1 |       1 |          0.04 |
| ollama:nomic-embed-text | dense                                        |     1 |          1 |        1 |       1 |          2.59 |
| ollama:nomic-embed-text | hybrid+rerank                                |     1 |          1 |        1 |       1 |          0.13 |

## hard (78 questions)

| config                                                                 | MRR               |   Recall@8 | nDCG@8            |   Hit@8 |   Latency (s) |
|:-----------------------------------------------------------------------|:------------------|-----------:|:------------------|--------:|--------------:|
| medcpt:ncbi/MedCPT | dense                                             | 0.934 [0.90-0.97] |          1 | 0.950 [0.92-0.98] |       1 |          0.02 |
| medcpt:ncbi/MedCPT | hybrid+rerank                                     | 0.931 [0.89-0.97] |          1 | 0.945 [0.91-0.97] |       1 |          0.05 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | dense                    | 0.947 [0.91-0.98] |          1 | 0.961 [0.93-0.98] |       1 |          0.02 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | hybrid+rerank            | 0.950 [0.91-0.98] |          1 | 0.960 [0.93-0.98] |       1 |          0.05 |
| sentence-transformers:intfloat/e5-base-v2 | dense                      | 0.968 [0.94-0.99] |          1 | 0.974 [0.95-0.99] |       1 |          0.02 |
| sentence-transformers:intfloat/e5-base-v2 | hybrid+rerank              | 0.952 [0.92-0.98] |          1 | 0.962 [0.94-0.98] |       1 |          0.05 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | dense         | 0.968 [0.94-0.99] |          1 | 0.976 [0.96-1.00] |       1 |          0.02 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | hybrid+rerank | 0.952 [0.92-0.98] |          1 | 0.962 [0.94-0.98] |       1 |          0.05 |
| ollama:nomic-embed-text | dense                                        | 0.955 [0.92-0.99] |          1 | 0.969 [0.95-0.99] |       1 |          2.15 |
| ollama:nomic-embed-text | hybrid+rerank                                | 0.946 [0.91-0.98] |          1 | 0.959 [0.93-0.98] |       1 |          0.14 |

## All questions

| config                                                                 |   MRR |   Recall |   nDCG |
|:-----------------------------------------------------------------------|------:|---------:|-------:|
| medcpt:ncbi/MedCPT | dense                                             | 0.895 |    0.934 |  0.905 |
| medcpt:ncbi/MedCPT | hybrid+rerank                                     | 0.942 |    0.977 |  0.95  |
| sentence-transformers:BAAI/bge-base-en-v1.5 | dense                    | 0.926 |    0.965 |  0.936 |
| sentence-transformers:BAAI/bge-base-en-v1.5 | hybrid+rerank            | 0.95  |    0.984 |  0.958 |
| sentence-transformers:intfloat/e5-base-v2 | dense                      | 0.928 |    0.957 |  0.935 |
| sentence-transformers:intfloat/e5-base-v2 | hybrid+rerank              | 0.947 |    0.988 |  0.957 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | dense         | 0.908 |    0.934 |  0.915 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | hybrid+rerank | 0.934 |    0.988 |  0.947 |
| ollama:nomic-embed-text | dense                                        | 0.928 |    0.965 |  0.938 |
| ollama:nomic-embed-text | hybrid+rerank                                | 0.951 |    0.988 |  0.96  |

## MRR by question type

| config                                                                 |   lookup_by_name |   lookup_by_mrn |   latest |   count_patient |   semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |
|:-----------------------------------------------------------------------|-----------------:|----------------:|---------:|----------------:|-----------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|
| medcpt:ncbi/MedCPT | dense                                             |                1 |               1 |        1 |               1 |          1 |                     0.95  |                  0.942 |        0.85  |                1 |                0.95  |          0.258 |                          1 |                        0.701 |
| medcpt:ncbi/MedCPT | hybrid+rerank                                     |                1 |               1 |        1 |               1 |          1 |                     0.912 |                  0.967 |        0.85  |                1 |                0.95  |          0.672 |                          1 |                        0.9   |
| sentence-transformers:BAAI/bge-base-en-v1.5 | dense                    |                1 |               1 |        1 |               1 |          1 |                     0.975 |                  0.942 |        0.875 |                1 |                0.925 |          0.473 |                          1 |                        0.85  |
| sentence-transformers:BAAI/bge-base-en-v1.5 | hybrid+rerank            |                1 |               1 |        1 |               1 |          1 |                     0.962 |                  0.967 |        0.875 |                1 |                0.925 |          0.727 |                          1 |                        0.9   |
| sentence-transformers:intfloat/e5-base-v2 | dense                      |                1 |               1 |        1 |               1 |          1 |                     1     |                  0.975 |        0.9   |                1 |                0.925 |          0.392 |                          1 |                        0.875 |
| sentence-transformers:intfloat/e5-base-v2 | hybrid+rerank              |                1 |               1 |        1 |               1 |          1 |                     0.962 |                  0.95  |        0.9   |                1 |                0.925 |          0.682 |                          1 |                        0.9   |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | dense         |                1 |               1 |        1 |               1 |          1 |                     0.975 |                  1     |        0.9   |                1 |                0.95  |          0.148 |                          1 |                        0.842 |
| sentence-transformers:NeuML/pubmedbert-base-embeddings | hybrid+rerank |                1 |               1 |        1 |               1 |          1 |                     0.938 |                  0.975 |        0.9   |                1 |                0.95  |          0.485 |                          1 |                        0.9   |
| ollama:nomic-embed-text | dense                                        |                1 |               1 |        1 |               1 |          1 |                     0.975 |                  0.95  |        0.9   |                1 |                0.925 |          0.418 |                          1 |                        0.9   |
| ollama:nomic-embed-text | hybrid+rerank                                |                1 |               1 |        1 |               1 |          1 |                     0.938 |                  0.95  |        0.9   |                1 |                0.925 |          0.754 |                          1 |                        0.9   |

## Cost

| model                                                  |   dim |   chunks |   build_s |   embed_s_per_1k_chunks |   model_ram_mb |   vectors_mb |   query_embed_ms |
|:-------------------------------------------------------|------:|---------:|----------:|------------------------:|---------------:|-------------:|-----------------:|
| medcpt:ncbi/MedCPT                                     |   768 |    15749 |   10249.7 |                   650.8 |              0 |         46.1 |              5.2 |
| sentence-transformers:BAAI/bge-base-en-v1.5            |   768 |    15749 |    7618.3 |                   483.7 |              0 |         46.1 |              8.2 |
| sentence-transformers:intfloat/e5-base-v2              |   768 |    15749 |    7270.2 |                   461.6 |              0 |         46.1 |              7   |
| sentence-transformers:NeuML/pubmedbert-base-embeddings |   768 |    15749 |     140.5 |                     8.9 |              0 |         46.1 |              7.5 |
| ollama:nomic-embed-text                                |   768 |    15749 |     682.8 |                    43.4 |              0 |         46.1 |           2129.3 |
