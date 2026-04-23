def clean_text(text: str) -> str:
    """Strip edges, normalize spaces within each line, keep line breaks so lists/multi-line input stay coherent."""
    text = text.strip()
    if not text:
        return text
    lines = []
    for line in text.splitlines():
        normalized = " ".join(line.split())
        if normalized:
            lines.append(normalized)
    return "\n".join(lines)
