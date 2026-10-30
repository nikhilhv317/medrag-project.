# Embedding model benchmark

Benchmark subset of the index (see medrag/eval/bench.py); compare rows with each other only.

## documents (80 questions)

| config                                                       | MRR               | Recall@8          | nDCG@8            | Hit@8             |   Latency (s) |
|:-------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense         | 0.787 [0.70-0.87] | 0.850 [0.77-0.93] | 0.803 [0.72-0.88] | 0.850 [0.77-0.93] |          0.12 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank | 0.855 [0.78-0.92] | 0.938 [0.89-0.99] | 0.876 [0.81-0.93] | 0.938 [0.89-0.99] |         12.93 |

## easy (100 questions)

| config                                                       |   MRR |   Recall@8 |   nDCG@8 |   Hit@8 |   Latency (s) |
|:-------------------------------------------------------------|------:|-----------:|---------:|--------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense         |     1 |          1 |        1 |       1 |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank |     1 |          1 |        1 |       1 |          1.65 |

## hard (78 questions)

| config                                                       | MRR               |   Recall@8 | nDCG@8            |   Hit@8 |   Latency (s) |
|:-------------------------------------------------------------|:------------------|-----------:|:------------------|--------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense         | 0.947 [0.91-0.98] |          1 | 0.961 [0.93-0.98] |       1 |          0.11 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank | 0.943 [0.90-0.98] |          1 | 0.955 [0.93-0.98] |       1 |          2.15 |

## All questions

| config                                                       |   MRR |   Recall |   nDCG |
|:-------------------------------------------------------------|------:|---------:|-------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense         | 0.918 |    0.953 |  0.927 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank | 0.938 |    0.981 |  0.948 |

## MRR by question type

| config                                                       |   lookup_by_name |   lookup_by_mrn |   latest |   count_patient |   semantic |   hard_paraphrase_patient |   hard_semantic_cohort |   hard_trend |   hard_typo_name |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |
|:-------------------------------------------------------------|-----------------:|----------------:|---------:|----------------:|-----------:|--------------------------:|-----------------------:|-------------:|-----------------:|---------------------:|---------------:|---------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense         |                1 |               1 |        1 |               1 |          1 |                     0.975 |                  0.942 |        0.875 |                1 |                0.975 |          0.298 |                          1 |                        0.875 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank |                1 |               1 |        1 |               1 |          1 |                     0.938 |                  0.967 |        0.875 |                1 |                0.975 |          0.546 |                          1 |                        0.9   |

## Cost

| model                                        |   dim |   chunks |   build_s |   embed_s_per_1k_chunks |   model_ram_mb |   vectors_mb |   query_embed_ms |
|:---------------------------------------------|------:|---------:|----------:|------------------------:|---------------:|-------------:|-----------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 |   384 |    15749 |       6.8 |                     nan |              0 |         23.1 |             51.5 |
