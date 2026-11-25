| model               | polarity   | condition              |   n |   parse_rate |   accuracy |   follow_rate |   flip_rate |   conflict_rate |   own_desc_acc |
|:--------------------|:-----------|:-----------------------|----:|-------------:|-----------:|--------------:|------------:|----------------:|---------------:|
| ollama/gemma3:4b    | contradict | Chart only             |  40 |        1.000 |      0.625 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b    | contradict | Caption                |  40 |        1.000 |      0.025 |         0.975 |       0.960 |           0.000 |        nan     |
| ollama/gemma3:4b    | contradict | User, bare             |  40 |        1.000 |      0.000 |         1.000 |       1.000 |         nan     |        nan     |
| ollama/gemma3:4b    | contradict | User, opinion          |  40 |        1.000 |      0.275 |         0.725 |       0.560 |           0.000 |        nan     |
| ollama/gemma3:4b    | contradict | User, expert           |  40 |        1.000 |      0.050 |         0.950 |       0.920 |           0.000 |        nan     |
| ollama/gemma3:4b    | contradict | Scripted own turn      |  40 |        1.000 |      0.000 |         1.000 |       1.000 |         nan     |        nan     |
| ollama/gemma3:4b    | contradict | Self-caption           |  40 |        1.000 |      0.475 |         0.525 |       0.400 |           0.000 |          0.774 |
| ollama/gemma3:4b    | contradict | Self-caption, no claim |  40 |        1.000 |      0.775 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b | contradict | Chart only             |  40 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b | contradict | Caption                |  40 |        1.000 |      0.875 |         0.125 |       0.125 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b | contradict | User, bare             |  40 |        1.000 |      0.900 |         0.100 |       0.100 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b | contradict | User, opinion          |  40 |        1.000 |      0.875 |         0.125 |       0.125 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b | contradict | User, expert           |  40 |        1.000 |      0.925 |         0.075 |       0.075 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b | contradict | Scripted own turn      |  40 |        1.000 |      0.875 |         0.125 |       0.125 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b | contradict | Self-caption           |  40 |        1.000 |      0.875 |         0.125 |       0.125 |           0.000 |          1.000 |
| ollama/qwen2.5vl:3b | contradict | Self-caption, no claim |  40 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b | contradict | Chart only             |  40 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b | contradict | Caption                |  40 |        1.000 |      0.900 |         0.100 |       0.100 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b | contradict | User, bare             |  40 |        1.000 |      0.925 |         0.075 |       0.075 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b | contradict | User, opinion          |  40 |        1.000 |      0.950 |         0.050 |       0.050 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b | contradict | User, expert           |  40 |        1.000 |      0.900 |         0.100 |       0.100 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b | contradict | Scripted own turn      |  40 |        1.000 |      0.700 |         0.300 |       0.300 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b | contradict | Self-caption           |  40 |        1.000 |      0.950 |         0.050 |       0.050 |           0.053 |          0.952 |
| ollama/qwen2.5vl:7b | contradict | Self-caption, no claim |  40 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
