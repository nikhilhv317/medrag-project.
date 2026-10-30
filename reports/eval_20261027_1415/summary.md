# MedRAG evaluation

Run: 2026-10-27 14:16

## Retrieval (k=8, 150 questions with known gold documents)

|                                            |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:-------------------------------------------|--------:|------:|-----------:|---------:|--------------:|
| ('hash:bow', 'bm25')                       |   1     | 0.661 |      1     |    0.749 |         0.04  |
| ('hash:bow', 'hybrid')                     |   1     | 0.659 |      1     |    0.748 |         0.041 |
| ('hash:bow', 'hybrid+rerank')              |   1     | 0.659 |      1     |    0.748 |         0.04  |
| ('hash:bow', 'dense')                      |   0.993 | 0.637 |      0.993 |    0.73  |         0.039 |
| ('hash:bow', 'hybrid+rerank (no filters)') |   0.527 | 0.219 |      0.527 |    0.291 |         0.107 |

### MRR by question type

|                                            |   count_patient |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:-------------------------------------------|----------------:|---------:|----------------:|-----------------:|-----------:|
| ('hash:bow', 'bm25')                       |           0.983 |    0.494 |           0.5   |            0.472 |      0.856 |
| ('hash:bow', 'dense')                      |           0.983 |    0.494 |           0.5   |            0.472 |      0.737 |
| ('hash:bow', 'hybrid')                     |           0.983 |    0.494 |           0.5   |            0.472 |      0.847 |
| ('hash:bow', 'hybrid+rerank')              |           0.983 |    0.494 |           0.5   |            0.472 |      0.847 |
| ('hash:bow', 'hybrid+rerank (no filters)') |           0.077 |    0.138 |           0.208 |            0.606 |      0.066 |
