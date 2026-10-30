# MedRAG evaluation

Run: 2026-10-27 14:29

## Retrieval (k=8, 150 questions with known gold documents)

| index    | mode                       |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:---------|:---------------------------|--------:|------:|-----------:|---------:|--------------:|
| hash:bow | bm25                       |   1     | 0.979 |      1     |    0.984 |         0.046 |
| hash:bow | hybrid                     |   1     | 0.978 |      1     |    0.983 |         0.049 |
| hash:bow | hybrid+rerank              |   1     | 0.978 |      1     |    0.983 |         0.043 |
| hash:bow | dense                      |   1     | 0.95  |      1     |    0.962 |         0.043 |
| hash:bow | hybrid+rerank (no filters) |   0.507 | 0.219 |      0.507 |    0.287 |         0.11  |

### MRR by question type

| index    | mode                       |   count_patient |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:---------|:---------------------------|----------------:|---------:|----------------:|-----------------:|-----------:|
| hash:bow | bm25                       |           0.983 |    1     |           1     |            1     |      0.911 |
| hash:bow | dense                      |           0.983 |    1     |           1     |            1     |      0.764 |
| hash:bow | hybrid                     |           0.983 |    1     |           1     |            1     |      0.906 |
| hash:bow | hybrid+rerank              |           0.983 |    1     |           1     |            1     |      0.906 |
| hash:bow | hybrid+rerank (no filters) |           0.08  |    0.137 |           0.188 |            0.623 |      0.067 |
