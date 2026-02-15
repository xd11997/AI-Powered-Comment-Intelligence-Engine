import random

def chunk_comments(comments, chunk_size=1000):
    comments_copy = comments.copy()
    random.shuffle(comments_copy)
    chunks = []
    for i in range(0, len(comments_copy), chunk_size):
        chunks.append(comments_copy[i:i+chunk_size])
    return chunks
