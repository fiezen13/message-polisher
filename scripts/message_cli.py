from app.services.text_service import clean_text

def main():
    message = input("Enter your message: ")
    message = clean_text(message)
    print("Cleaned message: ", message)

if __name__ == "__main__":
    main()

