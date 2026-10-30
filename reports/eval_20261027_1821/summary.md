# MedRAG evaluation

Run: 2026-10-27 19:01

## Retrieval (k=8, 150 questions with known gold documents)

| index                                        | mode                       |   Hit@8 |   MRR |   Recall@8 |   nDCG@8 |   Latency (s) |
|:---------------------------------------------|:---------------------------|--------:|------:|-----------:|---------:|--------------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                       |   1     | 0.997 |      1     |    0.998 |         0.081 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                     |   1     | 0.997 |      1     |    0.998 |         0.145 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank              |   1     | 0.997 |      1     |    0.998 |         0.517 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                      |   1     | 0.993 |      1     |    0.995 |         0.168 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (no filters) |   0.767 | 0.664 |      0.767 |    0.69  |         6.685 |

### MRR by question type

| index                                        | mode                       |   count_patient |   latest |   lookup_by_mrn |   lookup_by_name |   semantic |
|:---------------------------------------------|:---------------------------|----------------:|---------:|----------------:|-----------------:|-----------:|
| sentence-transformers:BAAI/bge-small-en-v1.5 | bm25                       |           1     |        1 |           1     |            1     |      0.983 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | dense                      |           1     |        1 |           1     |            1     |      0.967 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid                     |           1     |        1 |           1     |            1     |      0.983 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank              |           1     |        1 |           1     |            1     |      0.983 |
| sentence-transformers:BAAI/bge-small-en-v1.5 | hybrid+rerank (no filters) |           0.983 |        0 |           0.867 |            0.817 |      0.653 |

## Answers

| llm               |   fact_recall |   number_correct |   abstain_correct |   cites_sources |   retrieval_s |   generation_s |
|:------------------|--------------:|-----------------:|------------------:|----------------:|--------------:|---------------:|
| ollama:qwen2.5:3b |         0.789 |                1 |                 1 |           0.125 |         0.398 |         51.838 |

- fact_recall: share of key facts from the gold report present in the answer
- number_correct: count questions answered with the exact number
- abstain_correct: says 'not found' exactly when it should
- judge_*: 1-5 scores from the judge model (a different model from the one answering)
