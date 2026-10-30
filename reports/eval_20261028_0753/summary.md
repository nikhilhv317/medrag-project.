# MedRAG evaluation

Run: 2026-10-28 08:03

Numbers are means with bootstrap 95% confidence intervals in brackets.

## Retrieval (k=8)

### documents questions (80)

| config                                                                              | Hit@8             | MRR               | Recall@8          | nDCG@8            |   Latency (s) |
|:------------------------------------------------------------------------------------|:------------------|:------------------|:------------------|:------------------|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) | 0.875 [0.80-0.94] | 0.809 [0.73-0.88] | 0.875 [0.80-0.94] | 0.825 [0.75-0.89] |          7.43 |

### MRR by question type

| config                                                                              |   doc_patient_lookup |   doc_semantic |   doc_transcription_lookup |   doc_transcription_semantic |
|:------------------------------------------------------------------------------------|---------------------:|---------------:|---------------------------:|-----------------------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (MedCPT-Cross-Encoder) |                0.975 |          0.562 |                          1 |                          0.7 |
