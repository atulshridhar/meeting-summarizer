import os
import argparse
from dotenv import load_dotenv
from openai import OpenAIError

def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY") or None


def summarize_text(text: str, api_key: str) -> str:
    # If no real key, return stub for testing
    if api_key is None:
        return "[Stub summary for testing]"
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
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        # Gracefully handle API errors and rate limits
        print(f"Warning: LLM call failed: {e}. Using stub summary.")
        return "[Stub summary due to API error]"


def main():
    parser = argparse.ArgumentParser(
        description="Summarize meeting notes via LLM"
    )
    parser.add_argument("file", help="Path to notes.txt")
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
        summary = "[Stub summary for testing]"
    else:
        summary = summarize_text(notes, api_key)

    summary = summarize_text(notes, api_key)

    print("Summary:")
    print(summary)


if __name__ == "__main__":
    main()