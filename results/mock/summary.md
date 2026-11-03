> MOCK DATA from a simulated model. These numbers test the pipeline and mean nothing.

| model        | polarity   | condition        |   n |   parse_rate |   accuracy |   follow_rate |   flip_rate |   conflict_rate |
|:-------------|:-----------|:-----------------|----:|-------------:|-----------:|--------------:|------------:|----------------:|
| mock/mock-v1 | contradict | Chart only       | 200 |        1.000 |      0.970 |       nan     |     nan     |         nan     |
| mock/mock-v1 | contradict | Caption          | 200 |        1.000 |      0.765 |         0.235 |       0.242 |           0.523 |
| mock/mock-v1 | contradict | User claim       | 200 |        1.000 |      0.590 |         0.410 |       0.412 |           0.542 |
| mock/mock-v1 | contradict | Own earlier turn | 200 |        1.000 |      0.420 |         0.580 |       0.577 |           0.405 |
