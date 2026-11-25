# Planned comparisons (H1 to H3)

Charts each model read correctly with no claim only. rate_a and rate_b are flip rates on the
same charts, and p is an exact two-sided McNemar test. p_holm applies the Holm correction
across all of one model's planned tests (five comparisons in each wording it has).
A comparison counts as supported when the difference goes in the predicted direction
and p_holm < .05.

| model               | hypothesis   | setting    | comparison                     |   n |   rate_a |   rate_b |   only_a |   only_b |       p | direction_as_predicted   |   p_holm | supported   |
|:--------------------|:-------------|:-----------|:-------------------------------|----:|---------:|---------:|---------:|---------:|--------:|:-------------------------|---------:|:------------|
| ollama/gemma3:4b    | H1           | contradict | User, opinion < User, bare     |  25 |    0.56  |    1     |        0 |       11 | 0.00098 | True                     |  0.0039  | True        |
| ollama/gemma3:4b    | H1           | contradict | User, opinion < User, expert   |  25 |    0.56  |    0.92  |        0 |        9 | 0.0039  | True                     |  0.012   | True        |
| ollama/gemma3:4b    | H2           | contradict | Scripted own turn > Caption    |  25 |    1     |    0.96  |        1 |        0 | 1       | True                     |  1       | False       |
| ollama/gemma3:4b    | H2           | contradict | Scripted own turn > User, bare |  25 |    1     |    1     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/gemma3:4b    | H3           | contradict | Self-caption < User, bare      |  25 |    0.4   |    1     |        0 |       15 | 6.1e-05 | True                     |  0.00031 | True        |
| ollama/qwen2.5vl:3b | H1           | contradict | User, opinion < User, bare     |  40 |    0.125 |    0.1   |        1 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:3b | H1           | contradict | User, opinion < User, expert   |  40 |    0.125 |    0.075 |        2 |        0 | 0.5     | False                    |  1       | False       |
| ollama/qwen2.5vl:3b | H2           | contradict | Scripted own turn > Caption    |  40 |    0.125 |    0.125 |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:3b | H2           | contradict | Scripted own turn > User, bare |  40 |    0.125 |    0.1   |        1 |        0 | 1       | True                     |  1       | False       |
| ollama/qwen2.5vl:3b | H3           | contradict | Self-caption < User, bare      |  40 |    0.125 |    0.1   |        1 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b | H1           | contradict | User, opinion < User, bare     |  40 |    0.05  |    0.075 |        0 |        1 | 1       | True                     |  1       | False       |
| ollama/qwen2.5vl:7b | H1           | contradict | User, opinion < User, expert   |  40 |    0.05  |    0.1   |        0 |        2 | 0.5     | True                     |  1       | False       |
| ollama/qwen2.5vl:7b | H2           | contradict | Scripted own turn > Caption    |  40 |    0.3   |    0.1   |        8 |        0 | 0.0078  | True                     |  0.031   | True        |
| ollama/qwen2.5vl:7b | H2           | contradict | Scripted own turn > User, bare |  40 |    0.3   |    0.075 |        9 |        0 | 0.0039  | True                     |  0.02    | True        |
| ollama/qwen2.5vl:7b | H3           | contradict | Self-caption < User, bare      |  40 |    0.05  |    0.075 |        1 |        2 | 1       | True                     |  1       | False       |

## Summary by hypothesis

Number of wordings in which each planned comparison is supported. The specification
requires at least two of three wordings (for Gemini, which has one wording, one).

| model               | hypothesis   | comparison                     |   wordings_tested |   wordings_supported |
|:--------------------|:-------------|:-------------------------------|------------------:|---------------------:|
| ollama/gemma3:4b    | H1           | User, opinion < User, bare     |                 1 |                    1 |
| ollama/gemma3:4b    | H1           | User, opinion < User, expert   |                 1 |                    1 |
| ollama/gemma3:4b    | H2           | Scripted own turn > Caption    |                 1 |                    0 |
| ollama/gemma3:4b    | H2           | Scripted own turn > User, bare |                 1 |                    0 |
| ollama/gemma3:4b    | H3           | Self-caption < User, bare      |                 1 |                    1 |
| ollama/qwen2.5vl:3b | H1           | User, opinion < User, bare     |                 1 |                    0 |
| ollama/qwen2.5vl:3b | H1           | User, opinion < User, expert   |                 1 |                    0 |
| ollama/qwen2.5vl:3b | H2           | Scripted own turn > Caption    |                 1 |                    0 |
| ollama/qwen2.5vl:3b | H2           | Scripted own turn > User, bare |                 1 |                    0 |
| ollama/qwen2.5vl:3b | H3           | Self-caption < User, bare      |                 1 |                    0 |
| ollama/qwen2.5vl:7b | H1           | User, opinion < User, bare     |                 1 |                    0 |
| ollama/qwen2.5vl:7b | H1           | User, opinion < User, expert   |                 1 |                    0 |
| ollama/qwen2.5vl:7b | H2           | Scripted own turn > Caption    |                 1 |                    1 |
| ollama/qwen2.5vl:7b | H2           | Scripted own turn > User, bare |                 1 |                    1 |
| ollama/qwen2.5vl:7b | H3           | Self-caption < User, bare      |                 1 |                    0 |

# Cross-model comparisons

Same condition, two models, on charts both models read correctly with no claim (and only
the charts Gemini saw when Gemini is involved). p_holm treats all rows as one family.

| contrast   | setting    | condition         | model_a             | model_b             |   n |   rate_a |   rate_b |   only_a |   only_b |     p |   p_holm |
|:-----------|:-----------|:------------------|:--------------------|:--------------------|----:|---------:|---------:|---------:|---------:|------:|---------:|
| scale      | contradict | Caption           | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.125 |    0.1   |        1 |        0 | 1     |    1     |
| scale      | contradict | User, bare        | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.1   |    0.075 |        1 |        0 | 1     |    1     |
| scale      | contradict | User, opinion     | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.125 |    0.05  |        3 |        0 | 0.25  |    1     |
| scale      | contradict | User, expert      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.075 |    0.1   |        1 |        2 | 1     |    1     |
| scale      | contradict | Scripted own turn | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.125 |    0.3   |        0 |        7 | 0.016 |    0.094 |
| scale      | contradict | Self-caption      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b |  40 |    0.125 |    0.05  |        3 |        0 | 0.25  |    1     |

# Exploratory comparisons (not corrected)

| model               | setting    | comparison                        |   n |   rate_a |   rate_b |   only_a |   only_b |       p |
|:--------------------|:-----------|:----------------------------------|----:|---------:|---------:|---------:|---------:|--------:|
| ollama/gemma3:4b    | contradict | User, expert vs User, bare        |  25 |    0.92  |    1     |        0 |        2 | 0.5     |
| ollama/gemma3:4b    | contradict | Caption vs User, bare             |  25 |    0.96  |    1     |        0 |        1 | 1       |
| ollama/gemma3:4b    | contradict | Self-caption vs Scripted own turn |  25 |    0.4   |    1     |        0 |       15 | 6.1e-05 |
| ollama/qwen2.5vl:3b | contradict | User, expert vs User, bare        |  40 |    0.075 |    0.1   |        0 |        1 | 1       |
| ollama/qwen2.5vl:3b | contradict | Caption vs User, bare             |  40 |    0.125 |    0.1   |        1 |        0 | 1       |
| ollama/qwen2.5vl:3b | contradict | Self-caption vs Scripted own turn |  40 |    0.125 |    0.125 |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b | contradict | User, expert vs User, bare        |  40 |    0.1   |    0.075 |        2 |        1 | 1       |
| ollama/qwen2.5vl:7b | contradict | Caption vs User, bare             |  40 |    0.1   |    0.075 |        1 |        0 | 1       |
| ollama/qwen2.5vl:7b | contradict | Self-caption vs Scripted own turn |  40 |    0.05  |    0.3   |        0 |       10 | 0.002   |

# Flip rate by the chart's true direction

Does a false claim of growth work as well as a false claim of decline?

| model               | setting    | condition         |   claim says 'rose' (chart fell) |   claim says 'fell' (chart rose) |
|:--------------------|:-----------|:------------------|---------------------------------:|---------------------------------:|
| ollama/gemma3:4b    | contradict | Caption           |                            0.800 |                            1.000 |
| ollama/gemma3:4b    | contradict | Scripted own turn |                            1.000 |                            1.000 |
| ollama/gemma3:4b    | contradict | Self-caption      |                            0.400 |                            0.400 |
| ollama/gemma3:4b    | contradict | User, bare        |                            1.000 |                            1.000 |
| ollama/gemma3:4b    | contradict | User, expert      |                            0.600 |                            1.000 |
| ollama/gemma3:4b    | contradict | User, opinion     |                            0.200 |                            0.650 |
| ollama/qwen2.5vl:3b | contradict | Caption           |                            0.000 |                            0.250 |
| ollama/qwen2.5vl:3b | contradict | Scripted own turn |                            0.000 |                            0.250 |
| ollama/qwen2.5vl:3b | contradict | Self-caption      |                            0.000 |                            0.250 |
| ollama/qwen2.5vl:3b | contradict | User, bare        |                            0.000 |                            0.200 |
| ollama/qwen2.5vl:3b | contradict | User, expert      |                            0.000 |                            0.150 |
| ollama/qwen2.5vl:3b | contradict | User, opinion     |                            0.000 |                            0.250 |
| ollama/qwen2.5vl:7b | contradict | Caption           |                            0.000 |                            0.200 |
| ollama/qwen2.5vl:7b | contradict | Scripted own turn |                            0.000 |                            0.600 |
| ollama/qwen2.5vl:7b | contradict | Self-caption      |                            0.000 |                            0.100 |
| ollama/qwen2.5vl:7b | contradict | User, bare        |                            0.000 |                            0.150 |
| ollama/qwen2.5vl:7b | contradict | User, expert      |                            0.000 |                            0.200 |
| ollama/qwen2.5vl:7b | contradict | User, opinion     |                            0.000 |                            0.100 |
