import time
from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_article(transcript):
    for attempt in range(3):  # retry 3 times
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"""
Convert this transcript into a structured article:
- Title
- Introduction
- Key Points
- Conclusion

Transcript:
{transcript}
"""
            )
            return response.text

        except Exception as e:
            if "503" in str(e):
                time.sleep(5)  # wait before retry
            else:
                raise e

    raise Exception("Failed after multiple retries. Try again later.")