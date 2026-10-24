from detector import split_sentences, text_metrics, _heuristic_score


def test_split_sentences_handles_punctuation_and_newlines():
    assert split_sentences("Hello world. Another line!\nLast one") == [
        "Hello world.", "Another line!", "Last one"
    ]


def test_text_metrics_returns_expected_counts():
    metrics = text_metrics("One short sentence. Another longer sentence here!")
    assert metrics["word_count"] == 7
    assert metrics["sentence_count"] == 2
    assert metrics["character_count"] > 0
    assert 0 <= metrics["vocabulary_diversity"] <= 100


def test_heuristic_is_bounded_and_explained():
    score, cues = _heuristic_score(
        "Furthermore, this is a sentence. Moreover, this is another sentence. In conclusion, we finish."
        , text_metrics("Furthermore, this is a sentence. Moreover, this is another sentence. In conclusion, we finish.")
    )
    assert 5 <= score <= 95
    assert cues
