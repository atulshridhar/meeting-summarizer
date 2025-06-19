from src.summarizer import summarize_text

def test_summarize_text_stub():
    # Use stub summary path without real API key
    text = open('notes/alice_meeting.txt').read()
    summary = summarize_text(text, None)
    assert summary == "[Stub summary for testing]"
