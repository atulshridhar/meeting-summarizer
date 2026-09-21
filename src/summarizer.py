import os
import argparse
from dotenv import load_dotenv
from openai import OpenAIError

def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY") or None


def truncate_to_max_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def summarize_text(text: str, api_key: str, max_words: int = None) -> str:
    # If no real key, return stub for testing
    if api_key is None:
        summary = "[Stub summary for testing]"
        if max_words is not None:
            summary = truncate_to_max_words(summary, max_words)
        return summary
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize this meeting: {text}"}
            ],
            max_tokens=200,
            temperature=0.2,
        )
        summary = response.choices[0].message.content.strip()
    except OpenAIError as e:
        # Gracefully handle API errors and rate limits
        # handle logs + API errors and rate limits
        print(f"!!! Warning: LLM call failed: {e}. Using stub summary.")
        summary = "[Stub summary due to API error]"

    if max_words is not None:
        summary = truncate_to_max_words(summary, max_words)
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Summarize meeting notes via LLM"
    )
    parser.add_argument("file", help="Path to notes.txt")
    parser.add_argument(
        "--max-words",
        type=int,
        default=None,
        metavar="N",
        help="Cap the summary to at most N words",
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            notes = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    api_key = load_api_key()
    if api_key is None:
        print("Warning: No API key found. Using stub summary.")

    summary = summarize_text(notes, api_key, max_words=args.max_words)

    print("Summary:")
    print(summary)


if __name__ == "__main__":
    main()
