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
You are an AI system designed to extract platform-native audience intelligence to support content strategy decisions.

Below is a list of comments under a specific content topic.

Your task is to extract structured insights that help creators understand what resonates with audiences.

1) Identify up to 5 Content Themes.
   - Focus on what can guide content creation from where audience's attention to.
   - Ignore generic emotional reactions such as "I love this", emojis only, or short excitement phrases.
   - Only include themes clearly supported by repeated mentions.

2) Identify up to 3 Audience Identity Signals.
   - Capture patterns that describe who the engaged audience appears to be.
   - Only include signals explicitly observable in the comments.

3) Identify up to 3 Engagement Drivers.
   - Extract recurring reasons why audiences seem highly engaged.
   - These should reflect mechanisms that trigger engagement, not just topics.

4) Identify up to 3 Recurring Frustrations.
   - Capture repeated dissatisfaction, confusion, or requests expressed in comments.
   - If none are clearly present, return "N/A".

Rules:
- Only use information explicitly present in the comments.
- Do not invent patterns not grounded in the data.
- Be concise and specific.
- Output strictly in JSON format with the following structure:

{{
  "content_themes": [],
  "audience_identity_signals": [],
  "engagement_drivers": [],
  "audience_painpoints": []
}}

If no valid signals exist for a section, return an string "N/A" for that section.


Comments:
{joined_comments}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    return response.output_text
