| model                        | polarity               | condition              |   n |   parse_rate |   accuracy |   follow_rate |   flip_rate |   conflict_rate |   own_desc_acc |
|:-----------------------------|:-----------------------|:-----------------------|----:|-------------:|-----------:|--------------:|------------:|----------------:|---------------:|
| gemini/gemini-3.5-flash-lite | contradict             | Chart only             | 100 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | Caption                |  64 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | User, bare             | 100 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | User, opinion          | 100 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | User, expert           | 100 |        1.000 |      1.000 |         0.000 |       0.000 |           0.010 |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | Scripted own turn      |  64 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| gemini/gemini-3.5-flash-lite | contradict             | Self-caption           | 100 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |          1.000 |
| ollama/gemma3:4b             | consistent             | Chart only             | 200 |        1.000 |      0.845 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | Caption                | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | User, bare             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | User, opinion          | 200 |        1.000 |      0.945 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | User, expert           | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | Scripted own turn      | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | consistent             | Self-caption           | 200 |        1.000 |      0.970 |       nan     |     nan     |         nan     |          0.834 |
| ollama/gemma3:4b             | contradict             | Chart only             | 200 |        1.000 |      0.845 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | contradict             | Caption                | 200 |        1.000 |      0.410 |         0.590 |       0.515 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict             | User, bare             | 200 |        1.000 |      0.440 |         0.560 |       0.479 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict             | User, opinion          | 200 |        1.000 |      0.530 |         0.470 |       0.373 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict             | User, expert           | 200 |        1.000 |      0.360 |         0.640 |       0.574 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict             | Scripted own turn      | 200 |        1.000 |      0.375 |         0.625 |       0.556 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict             | Self-caption           | 200 |        1.000 |      0.585 |         0.415 |       0.308 |           0.000 |          0.834 |
| ollama/gemma3:4b             | contradict             | Self-caption, no claim | 200 |        1.000 |      0.830 |       nan     |     nan     |         nan     |        nan     |
| ollama/gemma3:4b             | contradict (increased) | Caption                | 200 |        1.000 |      0.365 |         0.635 |       0.568 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (increased) | User, bare             | 200 |        1.000 |      0.355 |         0.645 |       0.580 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (increased) | User, opinion          | 200 |        1.000 |      0.515 |         0.485 |       0.391 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (increased) | User, expert           | 200 |        1.000 |      0.345 |         0.655 |       0.592 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (increased) | Scripted own turn      | 200 |        1.000 |      0.310 |         0.690 |       0.633 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (increased) | Self-caption           | 200 |        1.000 |      0.330 |         0.670 |       0.609 |           0.000 |          0.834 |
| ollama/gemma3:4b             | contradict (went_up)   | Caption                | 200 |        1.000 |      0.430 |         0.570 |       0.491 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (went_up)   | User, bare             | 200 |        1.000 |      0.395 |         0.605 |       0.533 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (went_up)   | User, opinion          | 200 |        1.000 |      0.490 |         0.510 |       0.420 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (went_up)   | User, expert           | 200 |        1.000 |      0.335 |         0.665 |       0.604 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (went_up)   | Scripted own turn      | 200 |        1.000 |      0.345 |         0.655 |       0.592 |           0.000 |        nan     |
| ollama/gemma3:4b             | contradict (went_up)   | Self-caption           | 200 |        1.000 |      0.330 |         0.670 |       0.609 |           0.000 |          0.834 |
| ollama/qwen2.5vl:3b          | consistent             | Chart only             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | Caption                | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | User, bare             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | User, opinion          | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | User, expert           | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | Scripted own turn      | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | consistent             | Self-caption           | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |          1.000 |
| ollama/qwen2.5vl:3b          | contradict             | Chart only             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | Caption                | 200 |        1.000 |      0.990 |         0.010 |       0.010 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | User, bare             | 200 |        1.000 |      0.925 |         0.075 |       0.075 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | User, opinion          | 200 |        1.000 |      0.960 |         0.040 |       0.040 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | User, expert           | 200 |        1.000 |      0.980 |         0.020 |       0.020 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | Scripted own turn      | 200 |        1.000 |      0.770 |         0.230 |       0.230 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption           | 200 |        1.000 |      0.680 |         0.320 |       0.320 |           0.000 |          1.000 |
| ollama/qwen2.5vl:3b          | contradict             | Self-caption, no claim | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | Caption                | 200 |        1.000 |      0.950 |         0.050 |       0.050 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, bare             | 200 |        1.000 |      0.810 |         0.190 |       0.190 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, opinion          | 200 |        1.000 |      0.950 |         0.050 |       0.050 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | User, expert           | 200 |        1.000 |      0.970 |         0.030 |       0.030 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | Scripted own turn      | 200 |        1.000 |      0.570 |         0.430 |       0.430 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (increased) | Self-caption           | 200 |        1.000 |      0.590 |         0.410 |       0.410 |           0.000 |          1.000 |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Caption                | 200 |        1.000 |      0.945 |         0.055 |       0.055 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, bare             | 200 |        1.000 |      0.915 |         0.085 |       0.085 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, opinion          | 200 |        1.000 |      0.955 |         0.045 |       0.045 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | User, expert           | 200 |        1.000 |      0.960 |         0.040 |       0.040 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Scripted own turn      | 200 |        1.000 |      0.675 |         0.325 |       0.325 |           0.000 |        nan     |
| ollama/qwen2.5vl:3b          | contradict (went_up)   | Self-caption           | 200 |        1.000 |      0.525 |         0.475 |       0.475 |           0.000 |          1.000 |
| ollama/qwen2.5vl:7b          | consistent             | Chart only             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | Caption                | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | User, bare             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | User, opinion          | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | User, expert           | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | Scripted own turn      | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | consistent             | Self-caption           | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |          1.000 |
| ollama/qwen2.5vl:7b          | contradict             | Chart only             | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | Caption                | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | User, bare             | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | User, opinion          | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | User, expert           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | Scripted own turn      | 200 |        1.000 |      0.900 |         0.100 |       0.100 |           0.028 |        nan     |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.005 |          1.000 |
| ollama/qwen2.5vl:7b          | contradict             | Self-caption, no claim | 200 |        1.000 |      1.000 |       nan     |     nan     |         nan     |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | Caption                | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, bare             | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, opinion          | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | User, expert           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | Scripted own turn      | 200 |        1.000 |      0.660 |         0.340 |       0.340 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (increased) | Self-caption           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |          1.000 |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Caption                | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, bare             | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, opinion          | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | User, expert           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Scripted own turn      | 200 |        1.000 |      0.880 |         0.120 |       0.120 |           0.017 |        nan     |
| ollama/qwen2.5vl:7b          | contradict (went_up)   | Self-caption           | 200 |        1.000 |      1.000 |         0.000 |       0.000 |           0.000 |          1.000 |
