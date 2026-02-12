from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_insights_from_chunk(comment_chunk):
    """
    Input: list of comment strings
    Output: structured dict with themes, positive drivers, pain points
    """

    joined_comments = "\n".join(comment_chunk)

    prompt = f"""
You are an AI system extracting structured audience insights.

Below is a list of TikTok comments under a specific content topic.

Your task:
1. Identify up to 5 recurring audience interest themes.
2. Identify up to 3 positive content drivers.
3. Identify up to 3 recurring pain points.

Rules:
- Only use information explicitly present in comments.
- Do not invent themes.
- Be concise.
- Output strictly in JSON format.

Comments:
{joined_comments}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    return response.output_text
