from app.services.ai_service import generate_polished_message
from app.services.prompt_service import build_prompt
from app.services.text_service import clean_text

def main():
    message = input("Enter your message: ")

    message = clean_text(message)

    prompt = build_prompt(message)

    result = generate_polished_message(prompt)

    print("\n==== POLISHED MESSAGE ====\n")
    print(result)


if __name__ == "__main__":
    main()

