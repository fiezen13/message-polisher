def clean_text(text: str) -> str:
    text = text.strip()     # Remove leading and trailing whitespace
    text = text.replace('\n', ' ') # Replace newlines with spaces
    text = ' '.join(text.split()) # Replace multiple spaces with a single space
    return text

