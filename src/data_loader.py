import pandas as pd

def load_comments(path):
    df = pd.read_csv(path)
    return df["comment_text"].tolist()
