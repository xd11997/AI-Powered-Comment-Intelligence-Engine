import csv
import random

video_ids = [f"v{i}" for i in range(1, 11)]

positive_phrases = [
    "I love how authentic this feels.",
    "This is actually very relatable.",
    "Your editing style is so calming.",
    "This motivates me to improve my routine.",
    "I appreciate the honesty here.",
    "This feels realistic and doable.",
    "Your structure is very clear.",
    "I like how simple you keep things.",
    "This inspired me a lot.",
    "The pacing is perfect."
]

negative_phrases = [
    "This feels too sponsored.",
    "I wish you showed more detail.",
    "This seems unrealistic.",
    "Too many ads lately.",
    "It feels repetitive.",
    "Not practical for most people.",
    "The intro is too long.",
    "You could go deeper into this.",
    "This looks expensive.",
    "I expected more explanation."
]

neutral_phrases = [
    "Can you share more details?",
    "What camera do you use?",
    "Please make a part two.",
    "Can you link the products?",
    "I have a question about this.",
    "More content like this please.",
    "Can you show a weekend version?",
    "Do you have a template?",
    "How long does this take?",
    "What time do you usually start?"
]

all_comments = []

for vid in video_ids:
    for _ in range(50):  # 50 comments per video → total 500
        sentiment_choice = random.choice(["pos", "neg", "neu"])

        if sentiment_choice == "pos":
            comment = random.choice(positive_phrases)
        elif sentiment_choice == "neg":
            comment = random.choice(negative_phrases)
        else:
            comment = random.choice(neutral_phrases)

        all_comments.append([vid, comment])

with open("data/lifestyle_comments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["video_id", "comment_text"])
    writer.writerows(all_comments)

print("Generated 500 comments successfully.")
