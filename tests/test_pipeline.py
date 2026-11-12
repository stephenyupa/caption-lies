import pytest
from caption_lies.charts import generate
from caption_lies.conditions import CONDITIONS, NEEDS_DESCRIPTION, NO_CLAIM, VERB_SETS, build_messages, claim_direction, claim_sentence
from caption_lies.scoring import parse_reply, wilson


def test_parse_json():
    assert parse_reply('{"answer": "increase", "explanation": "up"}')[0] == "increase"
    assert parse_reply('Sure!\n```json\n{"answer": "Decrease", "explanation": "x"}\n```')[0] == "decrease"


def test_parse_fallback_and_failure():
    assert parse_reply("It clearly went down over the year.") == ("decrease", "It clearly went down over the year.", "keyword")
    assert parse_reply("It rose and then fell.")[0] is None
    assert parse_reply("")[0] is None


def test_generation_is_balanced_and_unambiguous(tmp_path):
    metas = generate(20, tmp_path, seed=1)
    assert sum(m.direction == "increase" for m in metas) == 10
    for m in metas:
        assert (m.end_value > m.start_value) == (m.direction == "increase")
        assert (tmp_path / m.image).exists()


def test_claim_contradicts_and_same_claim_everywhere(tmp_path):
    meta = vars(generate(2, tmp_path, seed=2)[0])
    assert claim_direction(meta, "contradict") != meta["direction"]
    assert claim_direction(meta, "consistent") == meta["direction"]
    texts = {}
    for cond in CONDITIONS:
        msgs = build_messages(meta, cond, tmp_path, own_description="The line goes down." if cond in NEEDS_DESCRIPTION else None)
        texts[cond] = " ".join(c["text"] for m in msgs for c in m["content"] if c["type"] == "text")
        assert sum(c["type"] == "image" for m in msgs for c in m["content"]) == 1
    claim = texts["caption"].split("Caption: ")[1].split("\n")[0]
    assert all(claim not in texts[c] for c in NO_CLAIM)
    assert all(claim in texts[c] for c in CONDITIONS if c not in NO_CLAIM)
    assert texts["user_opinion"].startswith("I think ")
    assert "analyst" in texts["user_expert"]
    assert "The line goes down." in texts["self_caption"]


def test_wilson():
    lo, hi = wilson(50, 100)
    assert 0.39 < lo < 0.41 and 0.59 < hi < 0.61


def test_verb_sets_change_only_the_verb(tmp_path):
    meta = vars(generate(2, tmp_path, seed=3)[0])
    claims = {v: claim_sentence(meta, "contradict", v) for v in VERB_SETS}
    assert len(set(claims.values())) == len(VERB_SETS)
    for v, text in claims.items():
        assert VERB_SETS[v][claim_direction(meta, "contradict")] in text


def test_holm_matches_hand_calculation():
    from analyze import holm

    # Sorted p: .005, .01, .03, .04 -> x4, x3, x2, x1, then made non-decreasing.
    assert holm([0.01, 0.04, 0.03, 0.005]) == pytest.approx([0.03, 0.06, 0.06, 0.02])


def test_cohen_kappa_matches_hand_calculation():
    from annotate import cohen_kappa

    # Observed agreement 0.75, chance agreement 0.5 -> kappa 0.5.
    assert cohen_kappa(["a", "a", "b", "b"], ["a", "b", "b", "b"]) == pytest.approx(0.5)
    assert cohen_kappa(["a", "b"], ["a", "b"]) == pytest.approx(1.0)
