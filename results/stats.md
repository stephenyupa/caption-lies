# Planned comparisons (H1 to H3)

Charts each model read correctly with no claim only. rate_a and rate_b are flip rates on the
same charts, and p is an exact two-sided McNemar test. p_holm applies the Holm correction
across all of one model's planned tests (five comparisons in each wording it has).
A comparison counts as supported when the difference goes in the predicted direction
and p_holm < .05.

| model                        | hypothesis   | setting                | comparison                     |   n |   rate_a |   rate_b |   only_a |   only_b |       p | direction_as_predicted   |   p_holm | supported   |
|:-----------------------------|:-------------|:-----------------------|:-------------------------------|----:|---------:|---------:|---------:|---------:|--------:|:-------------------------|---------:|:------------|
| gemini/gemini-3.5-flash-lite | H1           | contradict             | User, opinion < User, bare     | 100 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| gemini/gemini-3.5-flash-lite | H1           | contradict             | User, opinion < User, expert   | 100 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| gemini/gemini-3.5-flash-lite | H2           | contradict             | Scripted own turn > Caption    | 100 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| gemini/gemini-3.5-flash-lite | H2           | contradict             | Scripted own turn > User, bare | 100 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| gemini/gemini-3.5-flash-lite | H3           | contradict             | Self-caption < User, bare      | 100 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/gemma3:4b             | H1           | contradict             | User, opinion < User, bare     | 169 |    0.373 |    0.479 |        0 |       18 | 7.6e-06 | True                     |  7.6e-05 | True        |
| ollama/gemma3:4b             | H1           | contradict             | User, opinion < User, expert   | 169 |    0.373 |    0.574 |        0 |       34 | 1.2e-10 | True                     |  1.7e-09 | True        |
| ollama/gemma3:4b             | H2           | contradict             | Scripted own turn > Caption    | 169 |    0.556 |    0.515 |        8 |        1 | 0.039   | True                     |  0.078   | False       |
| ollama/gemma3:4b             | H2           | contradict             | Scripted own turn > User, bare | 169 |    0.556 |    0.479 |       14 |        1 | 0.00098 | True                     |  0.0059  | True        |
| ollama/gemma3:4b             | H3           | contradict             | Self-caption < User, bare      | 169 |    0.308 |    0.479 |       12 |       41 | 8.2e-05 | True                     |  0.00074 | True        |
| ollama/gemma3:4b             | H1           | contradict (increased) | User, opinion < User, bare     | 169 |    0.391 |    0.58  |        0 |       32 | 4.7e-10 | True                     |  6.1e-09 | True        |
| ollama/gemma3:4b             | H1           | contradict (increased) | User, opinion < User, expert   | 169 |    0.391 |    0.592 |        0 |       34 | 1.2e-10 | True                     |  1.7e-09 | True        |
| ollama/gemma3:4b             | H2           | contradict (increased) | Scripted own turn > Caption    | 169 |    0.633 |    0.568 |       12 |        1 | 0.0034  | True                     |  0.017   | True        |
| ollama/gemma3:4b             | H2           | contradict (increased) | Scripted own turn > User, bare | 169 |    0.633 |    0.58  |       10 |        1 | 0.012   | True                     |  0.047   | True        |
| ollama/gemma3:4b             | H3           | contradict (increased) | Self-caption < User, bare      | 169 |    0.609 |    0.58  |        5 |        0 | 0.062   | False                    |  0.078   | False       |
| ollama/gemma3:4b             | H1           | contradict (went_up)   | User, opinion < User, bare     | 169 |    0.42  |    0.533 |        0 |       19 | 3.8e-06 | True                     |  4.2e-05 | True        |
| ollama/gemma3:4b             | H1           | contradict (went_up)   | User, opinion < User, expert   | 169 |    0.42  |    0.604 |        0 |       31 | 9.3e-10 | True                     |  1.1e-08 | True        |
| ollama/gemma3:4b             | H2           | contradict (went_up)   | Scripted own turn > Caption    | 169 |    0.592 |    0.491 |       19 |        2 | 0.00022 | True                     |  0.0018  | True        |
| ollama/gemma3:4b             | H2           | contradict (went_up)   | Scripted own turn > User, bare | 169 |    0.592 |    0.533 |       12 |        2 | 0.013   | True                     |  0.047   | True        |
| ollama/gemma3:4b             | H3           | contradict (went_up)   | Self-caption < User, bare      | 169 |    0.609 |    0.533 |       13 |        0 | 0.00024 | False                    |  0.0018  | False       |
| ollama/qwen2.5vl:3b          | H1           | contradict             | User, opinion < User, bare     | 200 |    0.04  |    0.075 |        0 |        7 | 0.016   | True                     |  0.062   | False       |
| ollama/qwen2.5vl:3b          | H1           | contradict             | User, opinion < User, expert   | 200 |    0.04  |    0.02  |        4 |        0 | 0.12    | False                    |  0.38    | False       |
| ollama/qwen2.5vl:3b          | H2           | contradict             | Scripted own turn > Caption    | 200 |    0.23  |    0.01  |       44 |        0 | 1.1e-13 | True                     |  1e-12   | True        |
| ollama/qwen2.5vl:3b          | H2           | contradict             | Scripted own turn > User, bare | 200 |    0.23  |    0.075 |       31 |        0 | 9.3e-10 | True                     |  6.5e-09 | True        |
| ollama/qwen2.5vl:3b          | H3           | contradict             | Self-caption < User, bare      | 200 |    0.32  |    0.075 |       49 |        0 | 3.6e-15 | False                    |  4.3e-14 | False       |
| ollama/qwen2.5vl:3b          | H1           | contradict (increased) | User, opinion < User, bare     | 200 |    0.05  |    0.19  |        1 |       29 | 5.8e-08 | True                     |  3.5e-07 | True        |
| ollama/qwen2.5vl:3b          | H1           | contradict (increased) | User, opinion < User, expert   | 200 |    0.05  |    0.03  |        5 |        1 | 0.22    | False                    |  0.44    | False       |
| ollama/qwen2.5vl:3b          | H2           | contradict (increased) | Scripted own turn > Caption    | 200 |    0.43  |    0.05  |       76 |        0 | 2.6e-23 | True                     |  3.7e-22 | True        |
| ollama/qwen2.5vl:3b          | H2           | contradict (increased) | Scripted own turn > User, bare | 200 |    0.43  |    0.19  |       48 |        0 | 7.1e-15 | True                     |  7.8e-14 | True        |
| ollama/qwen2.5vl:3b          | H3           | contradict (increased) | Self-caption < User, bare      | 200 |    0.41  |    0.19  |       44 |        0 | 1.1e-13 | False                    |  1e-12   | False       |
| ollama/qwen2.5vl:3b          | H1           | contradict (went_up)   | User, opinion < User, bare     | 200 |    0.045 |    0.085 |        0 |        8 | 0.0078  | True                     |  0.039   | True        |
| ollama/qwen2.5vl:3b          | H1           | contradict (went_up)   | User, opinion < User, expert   | 200 |    0.045 |    0.04  |        3 |        2 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:3b          | H2           | contradict (went_up)   | Scripted own turn > Caption    | 200 |    0.325 |    0.055 |       54 |        0 | 1.1e-16 | True                     |  1.4e-15 | True        |
| ollama/qwen2.5vl:3b          | H2           | contradict (went_up)   | Scripted own turn > User, bare | 200 |    0.325 |    0.085 |       48 |        0 | 7.1e-15 | True                     |  7.8e-14 | True        |
| ollama/qwen2.5vl:3b          | H3           | contradict (went_up)   | Self-caption < User, bare      | 200 |    0.475 |    0.085 |       78 |        0 | 6.6e-24 | False                    |  9.9e-23 | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict             | User, opinion < User, bare     | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict             | User, opinion < User, expert   | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H2           | contradict             | Scripted own turn > Caption    | 200 |    0.1   |    0     |       20 |        0 | 1.9e-06 | True                     |  2.1e-05 | True        |
| ollama/qwen2.5vl:7b          | H2           | contradict             | Scripted own turn > User, bare | 200 |    0.1   |    0     |       20 |        0 | 1.9e-06 | True                     |  2.1e-05 | True        |
| ollama/qwen2.5vl:7b          | H3           | contradict             | Self-caption < User, bare      | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict (increased) | User, opinion < User, bare     | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict (increased) | User, opinion < User, expert   | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H2           | contradict (increased) | Scripted own turn > Caption    | 200 |    0.34  |    0     |       68 |        0 | 6.8e-21 | True                     |  1e-19   | True        |
| ollama/qwen2.5vl:7b          | H2           | contradict (increased) | Scripted own turn > User, bare | 200 |    0.34  |    0     |       68 |        0 | 6.8e-21 | True                     |  1e-19   | True        |
| ollama/qwen2.5vl:7b          | H3           | contradict (increased) | Self-caption < User, bare      | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict (went_up)   | User, opinion < User, bare     | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H1           | contradict (went_up)   | User, opinion < User, expert   | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |
| ollama/qwen2.5vl:7b          | H2           | contradict (went_up)   | Scripted own turn > Caption    | 200 |    0.12  |    0     |       24 |        0 | 1.2e-07 | True                     |  1.5e-06 | True        |
| ollama/qwen2.5vl:7b          | H2           | contradict (went_up)   | Scripted own turn > User, bare | 200 |    0.12  |    0     |       24 |        0 | 1.2e-07 | True                     |  1.5e-06 | True        |
| ollama/qwen2.5vl:7b          | H3           | contradict (went_up)   | Self-caption < User, bare      | 200 |    0     |    0     |        0 |        0 | 1       | False                    |  1       | False       |

## Summary by hypothesis

Number of wordings in which each planned comparison is supported. The specification
requires at least two of three wordings (for Gemini, which has one wording, one).

| model                        | hypothesis   | comparison                     |   wordings_tested |   wordings_supported |
|:-----------------------------|:-------------|:-------------------------------|------------------:|---------------------:|
| gemini/gemini-3.5-flash-lite | H1           | User, opinion < User, bare     |                 1 |                    0 |
| gemini/gemini-3.5-flash-lite | H1           | User, opinion < User, expert   |                 1 |                    0 |
| gemini/gemini-3.5-flash-lite | H2           | Scripted own turn > Caption    |                 1 |                    0 |
| gemini/gemini-3.5-flash-lite | H2           | Scripted own turn > User, bare |                 1 |                    0 |
| gemini/gemini-3.5-flash-lite | H3           | Self-caption < User, bare      |                 1 |                    0 |
| ollama/gemma3:4b             | H1           | User, opinion < User, bare     |                 3 |                    3 |
| ollama/gemma3:4b             | H1           | User, opinion < User, expert   |                 3 |                    3 |
| ollama/gemma3:4b             | H2           | Scripted own turn > Caption    |                 3 |                    2 |
| ollama/gemma3:4b             | H2           | Scripted own turn > User, bare |                 3 |                    3 |
| ollama/gemma3:4b             | H3           | Self-caption < User, bare      |                 3 |                    1 |
| ollama/qwen2.5vl:3b          | H1           | User, opinion < User, bare     |                 3 |                    2 |
| ollama/qwen2.5vl:3b          | H1           | User, opinion < User, expert   |                 3 |                    0 |
| ollama/qwen2.5vl:3b          | H2           | Scripted own turn > Caption    |                 3 |                    3 |
| ollama/qwen2.5vl:3b          | H2           | Scripted own turn > User, bare |                 3 |                    3 |
| ollama/qwen2.5vl:3b          | H3           | Self-caption < User, bare      |                 3 |                    0 |
| ollama/qwen2.5vl:7b          | H1           | User, opinion < User, bare     |                 3 |                    0 |
| ollama/qwen2.5vl:7b          | H1           | User, opinion < User, expert   |                 3 |                    0 |
| ollama/qwen2.5vl:7b          | H2           | Scripted own turn > Caption    |                 3 |                    3 |
| ollama/qwen2.5vl:7b          | H2           | Scripted own turn > User, bare |                 3 |                    3 |
| ollama/qwen2.5vl:7b          | H3           | Self-caption < User, bare      |                 3 |                    0 |

# Cross-model comparisons

Same condition, two models, on charts both models read correctly with no claim (and only
the charts Gemini saw when Gemini is involved). p_holm treats all rows as one family.

| contrast       | setting                | condition         | model_a             | model_b                      |   n |   rate_a |   rate_b |   only_a |   only_b |       p |   p_holm |
|:---------------|:-----------------------|:------------------|:--------------------|:-----------------------------|----:|---------:|---------:|---------:|---------:|--------:|---------:|
| scale          | contradict             | Caption           | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.01  |     0    |        2 |        0 | 0.5     |  0.5     |
| scale          | contradict             | User, bare        | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.075 |     0    |       15 |        0 | 6.1e-05 |  0.00061 |
| scale          | contradict             | User, opinion     | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.04  |     0    |        8 |        0 | 0.0078  |  0.039   |
| scale          | contradict             | User, expert      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.02  |     0    |        4 |        0 | 0.12    |  0.25    |
| scale          | contradict             | Scripted own turn | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.23  |     0.1  |       33 |        7 | 4.2e-05 |  0.00047 |
| scale          | contradict             | Self-caption      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.32  |     0    |       64 |        0 | 1.1e-19 |  2.4e-18 |
| scale          | contradict (increased) | Caption           | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.05  |     0    |       10 |        0 | 0.002   |  0.016   |
| scale          | contradict (increased) | User, bare        | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.19  |     0    |       38 |        0 | 7.3e-12 |  1.2e-10 |
| scale          | contradict (increased) | User, opinion     | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.05  |     0    |       10 |        0 | 0.002   |  0.016   |
| scale          | contradict (increased) | User, expert      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.03  |     0    |        6 |        0 | 0.031   |  0.094   |
| scale          | contradict (increased) | Scripted own turn | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.43  |     0.34 |       18 |        0 | 7.6e-06 |  9.9e-05 |
| scale          | contradict (increased) | Self-caption      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.41  |     0    |       82 |        0 | 4.1e-25 |  9.5e-24 |
| scale          | contradict (went_up)   | Caption           | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.055 |     0    |       11 |        0 | 0.00098 |  0.0088  |
| scale          | contradict (went_up)   | User, bare        | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.085 |     0    |       17 |        0 | 1.5e-05 |  0.00018 |
| scale          | contradict (went_up)   | User, opinion     | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.045 |     0    |        9 |        0 | 0.0039  |  0.023   |
| scale          | contradict (went_up)   | User, expert      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.04  |     0    |        8 |        0 | 0.0078  |  0.039   |
| scale          | contradict (went_up)   | Scripted own turn | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.325 |     0.12 |       41 |        0 | 9.1e-13 |  1.5e-11 |
| scale          | contradict (went_up)   | Self-caption      | ollama/qwen2.5vl:3b | ollama/qwen2.5vl:7b          | 200 |    0.475 |     0    |       95 |        0 | 5e-29   |  1.2e-27 |
| open vs hosted | contradict             | Caption           | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.529 |     0    |       46 |        0 | 2.8e-14 |  5.4e-13 |
| open vs hosted | contradict             | User, bare        | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.506 |     0    |       44 |        0 | 1.1e-13 |  2e-12   |
| open vs hosted | contradict             | User, opinion     | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.414 |     0    |       36 |        0 | 2.9e-11 |  4.4e-10 |
| open vs hosted | contradict             | User, expert      | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.575 |     0    |       50 |        0 | 1.8e-15 |  3.7e-14 |
| open vs hosted | contradict             | Scripted own turn | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.575 |     0    |       50 |        0 | 1.8e-15 |  3.7e-14 |
| open vs hosted | contradict             | Self-caption      | ollama/gemma3:4b    | gemini/gemini-3.5-flash-lite |  87 |    0.322 |     0    |       28 |        0 | 7.5e-09 |  1e-07   |

# Exploratory comparisons (not corrected)

| model                        | setting                | comparison                        |   n |   rate_a |   rate_b |   only_a |   only_b |       p |
|:-----------------------------|:-----------------------|:----------------------------------|----:|---------:|---------:|---------:|---------:|--------:|
| gemini/gemini-3.5-flash-lite | contradict             | User, expert vs User, bare        | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Caption vs User, bare             | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Self-caption vs Scripted own turn | 100 |    0     |    0     |        0 |        0 | 1       |
| ollama/gemma3:4b             | contradict             | User, expert vs User, bare        | 169 |    0.574 |    0.479 |       16 |        0 | 3.1e-05 |
| ollama/gemma3:4b             | contradict             | Caption vs User, bare             | 169 |    0.515 |    0.479 |        9 |        3 | 0.15    |
| ollama/gemma3:4b             | contradict             | Self-caption vs Scripted own turn | 169 |    0.308 |    0.556 |        2 |       44 | 3.1e-11 |
| ollama/gemma3:4b             | contradict (increased) | User, expert vs User, bare        | 169 |    0.592 |    0.58  |        4 |        2 | 0.69    |
| ollama/gemma3:4b             | contradict (increased) | Caption vs User, bare             | 169 |    0.568 |    0.58  |        1 |        3 | 0.62    |
| ollama/gemma3:4b             | contradict (increased) | Self-caption vs Scripted own turn | 169 |    0.609 |    0.633 |        2 |        6 | 0.29    |
| ollama/gemma3:4b             | contradict (went_up)   | User, expert vs User, bare        | 169 |    0.604 |    0.533 |       12 |        0 | 0.00049 |
| ollama/gemma3:4b             | contradict (went_up)   | Caption vs User, bare             | 169 |    0.491 |    0.533 |        1 |        8 | 0.039   |
| ollama/gemma3:4b             | contradict (went_up)   | Self-caption vs Scripted own turn | 169 |    0.609 |    0.592 |        4 |        1 | 0.38    |
| ollama/qwen2.5vl:3b          | contradict             | User, expert vs User, bare        | 200 |    0.02  |    0.075 |        0 |       11 | 0.00098 |
| ollama/qwen2.5vl:3b          | contradict             | Caption vs User, bare             | 200 |    0.01  |    0.075 |        0 |       13 | 0.00024 |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption vs Scripted own turn | 200 |    0.32  |    0.23  |       20 |        2 | 0.00012 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, expert vs User, bare        | 200 |    0.03  |    0.19  |        0 |       32 | 4.7e-10 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Caption vs User, bare             | 200 |    0.05  |    0.19  |        0 |       28 | 7.5e-09 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Self-caption vs Scripted own turn | 200 |    0.41  |    0.43  |        2 |        6 | 0.29    |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, expert vs User, bare        | 200 |    0.04  |    0.085 |        0 |        9 | 0.0039  |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Caption vs User, bare             | 200 |    0.055 |    0.085 |        1 |        7 | 0.07    |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Self-caption vs Scripted own turn | 200 |    0.475 |    0.325 |       30 |        0 | 1.9e-09 |
| ollama/qwen2.5vl:7b          | contradict             | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption vs Scripted own turn | 200 |    0     |    0.1   |        0 |       20 | 1.9e-06 |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | Self-caption vs Scripted own turn | 200 |    0     |    0.34  |        0 |       68 | 6.8e-21 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Self-caption vs Scripted own turn | 200 |    0     |    0.12  |        0 |       24 | 1.2e-07 |

# Flip rate by the chart's true direction

Does a false claim of growth work as well as a false claim of decline?

| model                        | setting                | condition         |   claim says 'rose' (chart fell) |   claim says 'fell' (chart rose) |
|:-----------------------------|:-----------------------|:------------------|---------------------------------:|---------------------------------:|
| gemini/gemini-3.5-flash-lite | contradict             | Caption           |                            0.000 |                            0.000 |
| gemini/gemini-3.5-flash-lite | contradict             | Scripted own turn |                            0.000 |                            0.000 |
| gemini/gemini-3.5-flash-lite | contradict             | Self-caption      |                            0.000 |                            0.000 |
| gemini/gemini-3.5-flash-lite | contradict             | User, bare        |                            0.000 |                            0.000 |
| gemini/gemini-3.5-flash-lite | contradict             | User, expert      |                            0.000 |                            0.000 |
| gemini/gemini-3.5-flash-lite | contradict             | User, opinion     |                            0.000 |                            0.000 |
| ollama/gemma3:4b             | contradict             | Caption           |                            0.043 |                            0.840 |
| ollama/gemma3:4b             | contradict             | Scripted own turn |                            0.087 |                            0.880 |
| ollama/gemma3:4b             | contradict             | Self-caption      |                            0.043 |                            0.490 |
| ollama/gemma3:4b             | contradict             | User, bare        |                            0.043 |                            0.780 |
| ollama/gemma3:4b             | contradict             | User, expert      |                            0.043 |                            0.940 |
| ollama/gemma3:4b             | contradict             | User, opinion     |                            0.029 |                            0.610 |
| ollama/gemma3:4b             | contradict (increased) | Caption           |                            0.043 |                            0.930 |
| ollama/gemma3:4b             | contradict (increased) | Scripted own turn |                            0.130 |                            0.980 |
| ollama/gemma3:4b             | contradict (increased) | Self-caption      |                            0.043 |                            1.000 |
| ollama/gemma3:4b             | contradict (increased) | User, bare        |                            0.043 |                            0.950 |
| ollama/gemma3:4b             | contradict (increased) | User, expert      |                            0.043 |                            0.970 |
| ollama/gemma3:4b             | contradict (increased) | User, opinion     |                            0.043 |                            0.630 |
| ollama/gemma3:4b             | contradict (went_up)   | Caption           |                            0.043 |                            0.800 |
| ollama/gemma3:4b             | contradict (went_up)   | Scripted own turn |                            0.058 |                            0.960 |
| ollama/gemma3:4b             | contradict (went_up)   | Self-caption      |                            0.043 |                            1.000 |
| ollama/gemma3:4b             | contradict (went_up)   | User, bare        |                            0.043 |                            0.870 |
| ollama/gemma3:4b             | contradict (went_up)   | User, expert      |                            0.043 |                            0.990 |
| ollama/gemma3:4b             | contradict (went_up)   | User, opinion     |                            0.043 |                            0.680 |
| ollama/qwen2.5vl:3b          | contradict             | Caption           |                            0.000 |                            0.020 |
| ollama/qwen2.5vl:3b          | contradict             | Scripted own turn |                            0.000 |                            0.460 |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption      |                            0.000 |                            0.640 |
| ollama/qwen2.5vl:3b          | contradict             | User, bare        |                            0.000 |                            0.150 |
| ollama/qwen2.5vl:3b          | contradict             | User, expert      |                            0.000 |                            0.040 |
| ollama/qwen2.5vl:3b          | contradict             | User, opinion     |                            0.000 |                            0.080 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Caption           |                            0.000 |                            0.100 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Scripted own turn |                            0.000 |                            0.860 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Self-caption      |                            0.000 |                            0.820 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, bare        |                            0.000 |                            0.380 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, expert      |                            0.000 |                            0.060 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, opinion     |                            0.000 |                            0.100 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Caption           |                            0.000 |                            0.110 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Scripted own turn |                            0.000 |                            0.650 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Self-caption      |                            0.000 |                            0.950 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, bare        |                            0.000 |                            0.170 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, expert      |                            0.000 |                            0.080 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, opinion     |                            0.000 |                            0.090 |
| ollama/qwen2.5vl:7b          | contradict             | Caption           |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict             | Scripted own turn |                            0.000 |                            0.200 |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict             | User, bare        |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict             | User, expert      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict             | User, opinion     |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (increased) | Caption           |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (increased) | Scripted own turn |                            0.000 |                            0.680 |
| ollama/qwen2.5vl:7b          | contradict (increased) | Self-caption      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, bare        |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, expert      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, opinion     |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Caption           |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Scripted own turn |                            0.000 |                            0.240 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Self-caption      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, bare        |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, expert      |                            0.000 |                            0.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, opinion     |                            0.000 |                            0.000 |
