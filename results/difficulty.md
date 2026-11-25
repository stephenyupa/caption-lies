# Chart ground-truth checks

200 of 200 charts pass all three direction checks (endpoints, least-squares slope, order of minimum and maximum).

| measure | min | median | max |
|:--|--:|--:|--:|
| size of change (%) | 14.9 | 37.7 | 60.0 |
| variance explained by a straight line (%) | 88.8 | 96.4 | 99.7 |
| steps moving with the trend (%) | 55 | 86 | 100 |

# Visual difficulty (exploratory)

Logistic regression of following the false claim, rising charts only, standard errors clustered
by chart. An odds ratio above 1 means deference rises with the predictor.

| model               | predictor                      |   answers |   charts |   odds_ratio |   ci_low |   ci_high |       p |   flip_cleanest_third |   flip_noisiest_third |
|:--------------------|:-------------------------------|----------:|---------:|-------------:|---------:|----------:|--------:|----------------------:|----------------------:|
| ollama/gemma3:4b    | noise (per percentage point)   |      1800 |      100 |        1.225 |    1.072 |     1.4   | 0.0029  |                 0.81  |                 0.896 |
| ollama/gemma3:4b    | size of change (per 10 points) |      1800 |      100 |        0.961 |    0.766 |     1.206 | 0.73    |                 0.81  |                 0.896 |
| ollama/qwen2.5vl:3b | noise (per percentage point)   |      1800 |      100 |        1.308 |    1.115 |     1.535 | 0.00098 |                 0.284 |                 0.412 |
| ollama/qwen2.5vl:3b | size of change (per 10 points) |      1800 |      100 |        1.108 |    0.86  |     1.427 | 0.43    |                 0.284 |                 0.412 |
| ollama/qwen2.5vl:7b | noise (per percentage point)   |       300 |      100 |        1.166 |    1.008 |     1.35  | 0.038   |                 0.402 |                 0.394 |
| ollama/qwen2.5vl:7b | size of change (per 10 points) |       300 |      100 |        0.752 |    0.555 |     1.017 | 0.064   |                 0.402 |                 0.394 |
