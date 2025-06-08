def split_to_chunks(text, min_words=100, max_words=1000):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + max_words]
        if len(chunk) >= min_words:
            chunks.append(" ".join(chunk))
        i += max_words
    return chunks
