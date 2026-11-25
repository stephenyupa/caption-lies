# Chart ground-truth checks

40 of 40 charts pass all three direction checks (endpoints, least-squares slope, order of minimum and maximum).

| measure | min | median | max |
|:--|--:|--:|--:|
| size of change (%) | 15.2 | 39.5 | 286.3 |
| variance explained by a straight line (%) | 51.8 | 79.4 | 99.8 |
| steps moving with the trend (%) | 36 | 80 | 100 |

# Visual difficulty (exploratory)

Logistic regression of following the false claim, rising charts only, standard errors clustered
by chart. An odds ratio above 1 means deference rises with the predictor.

| model               | predictor                      |   answers |   charts |   odds_ratio |   ci_low |   ci_high |      p |   flip_cleanest_third |   flip_noisiest_third |
|:--------------------|:-------------------------------|----------:|---------:|-------------:|---------:|----------:|-------:|----------------------:|----------------------:|
| ollama/gemma3:4b    | noise (per percentage point)   |       120 |       20 |        1.04  |    0.995 |     1.087 | 0.086  |                 0.786 |                 0.944 |
| ollama/gemma3:4b    | size of change (per 10 points) |       120 |       20 |        1.018 |    0.9   |     1.152 | 0.77   |                 0.786 |                 0.944 |
| ollama/qwen2.5vl:3b | noise (per percentage point)   |       120 |       20 |        1.147 |    1.023 |     1.286 | 0.019  |                 0     |                 0.583 |
| ollama/qwen2.5vl:3b | size of change (per 10 points) |       120 |       20 |        0.902 |    0.685 |     1.189 | 0.47   |                 0     |                 0.583 |
| ollama/qwen2.5vl:7b | noise (per percentage point)   |       120 |       20 |        1.094 |    1.024 |     1.169 | 0.0082 |                 0.048 |                 0.472 |
| ollama/qwen2.5vl:7b | size of change (per 10 points) |       120 |       20 |        0.91  |    0.752 |     1.101 | 0.33   |                 0.048 |                 0.472 |
