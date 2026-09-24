from src.summarizer import summarize_text, truncate_to_max_words

def test_summarize_text_stub():
    summary = summarize_text("Alice and Bob discussed the project timeline.", None)
    assert summary == "[Stub summary for testing]"


def test_truncate_to_max_words_under_limit():
    text = "one two three"
    assert truncate_to_max_words(text, 5) == "one two three"


def test_truncate_to_max_words_exactly_at_limit():
    text = "one two three"
    assert truncate_to_max_words(text, 3) == "one two three"


def test_truncate_to_max_words_over_limit():
    text = "one two three four five"
    result = truncate_to_max_words(text, 3)
    assert result == "one two three"
    assert len(result.split()) == 3


def test_summarize_text_max_words_truncates():
    # Stub returns "[Stub summary for testing]" (4 words); cap to 2
    summary = summarize_text("some meeting notes", None, max_words=2)
    assert len(summary.split()) == 2
    assert summary == "[Stub summary"


def test_summarize_text_max_words_no_truncation_needed():
    # Stub is "[Stub summary for testing]" (4 words), max_words=10 → no change
    summary = summarize_text("some meeting notes", None, max_words=10)
    assert summary == "[Stub summary for testing]"


def test_summarize_text_max_words_none_returns_full():
    summary = summarize_text("some meeting notes", None, max_words=None)
    assert summary == "[Stub summary for testing]"
