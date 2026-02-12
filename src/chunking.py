def chunk_comments(comments, chunk_size=50):
    chunks = []
    for i in range(0, len(comments), chunk_size):
        chunks.append(comments[i:i+chunk_size])
    return chunks
