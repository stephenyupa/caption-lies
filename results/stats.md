# Paired comparisons

Charts each model read correctly with no claim only. Each row compares the flip rate
in two conditions on the same charts; p is an exact two-sided McNemar test.

| model                        | setting                | comparison                        |   n |   rate_a |   rate_b |   only_a |   only_b |       p |
|:-----------------------------|:-----------------------|:----------------------------------|----:|---------:|---------:|---------:|---------:|--------:|
| gemini/gemini-3.5-flash-lite | contradict             | User, opinion vs User, bare       | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | User, expert vs User, bare        | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | User, expert vs User, opinion     | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Caption vs User, bare             |  64 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Scripted own turn vs User, bare   |  64 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Self-caption vs User, bare        | 100 |    0     |    0     |        0 |        0 | 1       |
| gemini/gemini-3.5-flash-lite | contradict             | Self-caption vs Scripted own turn |  64 |    0     |    0     |        0 |        0 | 1       |
| ollama/gemma3:4b             | contradict             | User, opinion vs User, bare       | 169 |    0.373 |    0.479 |        0 |       18 | 7.6e-06 |
| ollama/gemma3:4b             | contradict             | User, expert vs User, bare        | 169 |    0.574 |    0.479 |       16 |        0 | 3.1e-05 |
| ollama/gemma3:4b             | contradict             | User, expert vs User, opinion     | 169 |    0.574 |    0.373 |       34 |        0 | 1.2e-10 |
| ollama/gemma3:4b             | contradict             | Caption vs User, bare             | 169 |    0.515 |    0.479 |        9 |        3 | 0.15    |
| ollama/gemma3:4b             | contradict             | Scripted own turn vs User, bare   | 169 |    0.556 |    0.479 |       14 |        1 | 0.00098 |
| ollama/gemma3:4b             | contradict             | Self-caption vs User, bare        | 169 |    0.308 |    0.479 |       12 |       41 | 8.2e-05 |
| ollama/gemma3:4b             | contradict             | Self-caption vs Scripted own turn | 169 |    0.308 |    0.556 |        2 |       44 | 3.1e-11 |
| ollama/gemma3:4b             | contradict (increased) | User, opinion vs User, bare       | 169 |    0.391 |    0.58  |        0 |       32 | 4.7e-10 |
| ollama/gemma3:4b             | contradict (increased) | User, expert vs User, bare        | 169 |    0.592 |    0.58  |        4 |        2 | 0.69    |
| ollama/gemma3:4b             | contradict (increased) | User, expert vs User, opinion     | 169 |    0.592 |    0.391 |       34 |        0 | 1.2e-10 |
| ollama/gemma3:4b             | contradict (increased) | Caption vs User, bare             | 169 |    0.568 |    0.58  |        1 |        3 | 0.62    |
| ollama/gemma3:4b             | contradict (increased) | Scripted own turn vs User, bare   | 169 |    0.633 |    0.58  |       10 |        1 | 0.012   |
| ollama/gemma3:4b             | contradict (increased) | Self-caption vs User, bare        | 169 |    0.609 |    0.58  |        5 |        0 | 0.062   |
| ollama/gemma3:4b             | contradict (increased) | Self-caption vs Scripted own turn | 169 |    0.609 |    0.633 |        2 |        6 | 0.29    |
| ollama/gemma3:4b             | contradict (went_up)   | User, opinion vs User, bare       | 169 |    0.42  |    0.533 |        0 |       19 | 3.8e-06 |
| ollama/gemma3:4b             | contradict (went_up)   | User, expert vs User, bare        | 169 |    0.604 |    0.533 |       12 |        0 | 0.00049 |
| ollama/gemma3:4b             | contradict (went_up)   | User, expert vs User, opinion     | 169 |    0.604 |    0.42  |       31 |        0 | 9.3e-10 |
| ollama/gemma3:4b             | contradict (went_up)   | Caption vs User, bare             | 169 |    0.491 |    0.533 |        1 |        8 | 0.039   |
| ollama/gemma3:4b             | contradict (went_up)   | Scripted own turn vs User, bare   | 169 |    0.592 |    0.533 |       12 |        2 | 0.013   |
| ollama/gemma3:4b             | contradict (went_up)   | Self-caption vs User, bare        | 169 |    0.609 |    0.533 |       13 |        0 | 0.00024 |
| ollama/gemma3:4b             | contradict (went_up)   | Self-caption vs Scripted own turn | 169 |    0.609 |    0.592 |        4 |        1 | 0.38    |
| ollama/qwen2.5vl:3b          | contradict             | User, opinion vs User, bare       | 200 |    0.04  |    0.075 |        0 |        7 | 0.016   |
| ollama/qwen2.5vl:3b          | contradict             | User, expert vs User, bare        | 200 |    0.02  |    0.075 |        0 |       11 | 0.00098 |
| ollama/qwen2.5vl:3b          | contradict             | User, expert vs User, opinion     | 200 |    0.02  |    0.04  |        0 |        4 | 0.12    |
| ollama/qwen2.5vl:3b          | contradict             | Caption vs User, bare             | 200 |    0.01  |    0.075 |        0 |       13 | 0.00024 |
| ollama/qwen2.5vl:3b          | contradict             | Scripted own turn vs User, bare   | 200 |    0.23  |    0.075 |       31 |        0 | 9.3e-10 |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption vs User, bare        | 200 |    0.32  |    0.075 |       49 |        0 | 3.6e-15 |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption vs Scripted own turn | 200 |    0.32  |    0.23  |       20 |        2 | 0.00012 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, opinion vs User, bare       | 200 |    0.05  |    0.19  |        1 |       29 | 5.8e-08 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, expert vs User, bare        | 200 |    0.03  |    0.19  |        0 |       32 | 4.7e-10 |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, expert vs User, opinion     | 200 |    0.03  |    0.05  |        1 |        5 | 0.22    |
| ollama/qwen2.5vl:3b          | contradict (increased) | Caption vs User, bare             | 200 |    0.05  |    0.19  |        0 |       28 | 7.5e-09 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Scripted own turn vs User, bare   | 200 |    0.43  |    0.19  |       48 |        0 | 7.1e-15 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Self-caption vs User, bare        | 200 |    0.41  |    0.19  |       44 |        0 | 1.1e-13 |
| ollama/qwen2.5vl:3b          | contradict (increased) | Self-caption vs Scripted own turn | 200 |    0.41  |    0.43  |        2 |        6 | 0.29    |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, opinion vs User, bare       | 200 |    0.045 |    0.085 |        0 |        8 | 0.0078  |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, expert vs User, bare        | 200 |    0.04  |    0.085 |        0 |        9 | 0.0039  |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, expert vs User, opinion     | 200 |    0.04  |    0.045 |        2 |        3 | 1       |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Caption vs User, bare             | 200 |    0.055 |    0.085 |        1 |        7 | 0.07    |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Scripted own turn vs User, bare   | 200 |    0.325 |    0.085 |       48 |        0 | 7.1e-15 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Self-caption vs User, bare        | 200 |    0.475 |    0.085 |       78 |        0 | 6.6e-24 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Self-caption vs Scripted own turn | 200 |    0.475 |    0.325 |       30 |        0 | 1.9e-09 |
| ollama/qwen2.5vl:7b          | contradict             | User, opinion vs User, bare       | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | User, expert vs User, opinion     | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | Scripted own turn vs User, bare   | 200 |    0.1   |    0     |       20 |        0 | 1.9e-06 |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption vs Scripted own turn | 200 |    0     |    0.1   |        0 |       20 | 1.9e-06 |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, opinion vs User, bare       | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, expert vs User, opinion     | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | Scripted own turn vs User, bare   | 200 |    0.34  |    0     |       68 |        0 | 6.8e-21 |
| ollama/qwen2.5vl:7b          | contradict (increased) | Self-caption vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (increased) | Self-caption vs Scripted own turn | 200 |    0     |    0.34  |        0 |       68 | 6.8e-21 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, opinion vs User, bare       | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, expert vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, expert vs User, opinion     | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Caption vs User, bare             | 200 |    0     |    0     |        0 |        0 | 1       |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Scripted own turn vs User, bare   | 200 |    0.12  |    0     |       24 |        0 | 1.2e-07 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Self-caption vs User, bare        | 200 |    0     |    0     |        0 |        0 | 1       |
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
