# Annotation results

Share (%) of annotated replies with each label (Table 4).

| model                 |   repair |   adopt |   hedge |   silent |   self-contradiction |   n |
|:----------------------|---------:|--------:|--------:|---------:|---------------------:|----:|
| Gemini 3.5 Flash Lite |      3.3 |     0   |       0 |     96.7 |                  0   |  30 |
| Gemma 3 4B            |      0   |     0   |       0 |     76.7 |                 23.3 |  30 |
| Qwen2.5-VL 3B         |      0   |     3.3 |       0 |     73.3 |                 23.3 |  30 |
| Qwen2.5-VL 7B         |      0   |     0   |       0 |    100   |                  0   |  30 |

## Counts by condition

| condition       |   repair |   adopt |   hedge |   silent |   self-contradiction |
|:----------------|---------:|--------:|--------:|---------:|---------------------:|
| caption         |        0 |       0 |       0 |       17 |                    3 |
| prior_assistant |        0 |       0 |       0 |       18 |                    2 |
| self_caption    |        0 |       1 |       0 |       15 |                    4 |
| user_claim      |        0 |       0 |       0 |       19 |                    1 |
| user_expert     |        1 |       0 |       0 |       18 |                    1 |
| user_opinion    |        0 |       0 |       0 |       17 |                    3 |

## Intra-annotator agreement

Not yet: run `python annotate.py recode` and label that sheet.

## Keyword detector check

Hand labels repair or hedge count as mentioning the conflict.

Detector flagged 1 replies; 1 of them mention the conflict (precision 1.00).
Of 1 replies that mention the conflict, it caught 1 (recall 1.00).
