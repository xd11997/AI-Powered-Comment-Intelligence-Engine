import random

def sample_comments(comments, n=40, seed=42):
    random.seed(seed)
    return random.sample(comments, min(n, len(comments)))
