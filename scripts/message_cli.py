import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.ai_service import generate_polished_message
from app.services.text_service import clean_text

def main():
    try:
        user_input = input("Enter your message: ").strip()
        if not user_input:
            print("Error: No input provided. Please enter a message.")
            return
        style_mode = input(
            "Style mode [neutral_business/formal_keigo/casual_polite] (default: neutral_business): "
        ).strip() or "neutral_business"
        cleaned_input = clean_text(user_input)
        print("Processing your message...")
        polished_message = generate_polished_message(cleaned_input, style_mode=style_mode)
        print("\nPolished Message:")
        print(polished_message)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

