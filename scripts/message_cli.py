from app.services.prompt_service import build_prompt
from app.services.text_service import clean_text

def main():
    message = input("Enter your message: ")

    message = clean_text(message)

    prompt = build_prompt(message)

    print("\n==== GENERATED PROMPT ====\n")
    print(prompt)

    print("\n==== CLEANED MESSAGE ====\n")
    print(message)

if __name__ == "__main__":
    main()

