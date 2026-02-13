from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

def clean_comments(df):
    df = df[["comment_text"]].copy()
    df["comment_text"] = df["comment_text"].str.replace(r"http\S+", "", regex=True)
    df["comment_text"] = df["comment_text"].str.strip()
    df = df[df["comment_text"].str.len() > 5]
    df = df[df["comment_text"].str.len() < 300]
    df = df[df['comment_text'].apply(is_english)]
    df = df.reset_index(drop=True)
    return df
