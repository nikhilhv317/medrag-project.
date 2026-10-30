# MedRAG evaluation

Run: 2026-10-27 18:18

## Retrieval (k=8, 150 questions with known gold documents)

| index                                        | mode                       |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:---------------------------------------------|:---------------------------|--------:|------:|-----------:|---------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank              |   1     | 0.987 |      1     |    0.99  |         0.389 |
| hash:bow                                     | hybrid+rerank              |   1     | 0.987 |      1     |    0.99  |         0.342 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                       |   1     | 0.979 |      1     |    0.984 |         0.042 |
| hash:bow                                     | bm25                       |   1     | 0.979 |      1     |    0.984 |         0.042 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                     |   1     | 0.978 |      1     |    0.983 |         0.092 |
| hash:bow                                     | hybrid                     |   1     | 0.978 |      1     |    0.983 |         0.042 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                      |   1     | 0.967 |      1     |    0.975 |         0.092 |
| hash:bow                                     | dense                      |   1     | 0.95  |      1     |    0.962 |         0.04  |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (no filters) |   0.713 | 0.645 |      0.713 |    0.662 |         5.679 |
| hash:bow                                     | hybrid+rerank (no filters) |   0.707 | 0.644 |      0.707 |    0.66  |         6.091 |

### MRR by question type

| index                                        | mode                       |   count_patient |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:---------------------------------------------|:---------------------------|----------------:|---------:|----------------:|-----------------:|-----------:|
| hash:bow                                     | bm25                       |           0.983 |        1 |           1     |            1     |      0.911 |
| hash:bow                                     | dense                      |           0.983 |        1 |           1     |            1     |      0.764 |
| hash:bow                                     | hybrid                     |           0.983 |        1 |           1     |            1     |      0.906 |
| hash:bow                                     | hybrid+rerank              |           0.983 |        1 |           1     |            1     |      0.95  |
| hash:bow                                     | hybrid+rerank (no filters) |           0.933 |        0 |           0.906 |            0.883 |      0.5   |
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                       |           0.983 |        1 |           1     |            1     |      0.911 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                      |           0.983 |        1 |           1     |            1     |      0.849 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                     |           0.983 |        1 |           1     |            1     |      0.906 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank              |           0.983 |        1 |           1     |            1     |      0.95  |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (no filters) |           0.978 |        0 |           0.911 |            0.883 |      0.451 |

## Answers

| llm               |   fact_recall |   number_correct |   abstain_correct |   cites_sources |   retrieval_s |   generation_s |
|:------------------|--------------:|-----------------:|------------------:|----------------:|--------------:|---------------:|
| ollama:qwen2.5:3b |         0.812 |             0.75 |                 1 |            0.25 |         0.619 |         58.077 |

- fact_recall: share of key facts from the gold report present in the answer
- number_correct: count questions answered with the exact number
- abstain_correct: says 'not found' exactly when it should
- judge_*: 1-5 scores from the judge model (a different model from the one answering)
