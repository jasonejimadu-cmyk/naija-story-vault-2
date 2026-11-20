
import os
import time
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing.")

MODEL = "gemini-2.5-flash"

PROMPT = """
Write an original, captivating Nigerian drama story.

Requirements:
- Use simple English mixed naturally with Nigerian Pidgin.
- Set the story in Nigeria.
- Include believable Nigerian characters.
- Start with a powerful hook.
- Include emotional dialogue and suspense.
- Make the story entertaining and original.
- Give it a memorable ending.
- Include a suitable title.

Return the complete story only.
"""

def generate_story():
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODEL}:generateContent?key={API_KEY}"
    )

    for attempt in range(5):
        try:
            response = requests.post(
                url,
                json={
                    "contents": [{
                        "parts": [{"text": PROMPT}]
                    }]
                },
                timeout=90
            )

            if response.status_code in (429, 500, 502, 503, 504):
                print(f"Temporary error: {response.status_code}")
                time.sleep(10 * (attempt + 1))
                continue

            response.raise_for_status()
            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except requests.RequestException as error:
            print(f"Attempt {attempt + 1}: {error}")
            time.sleep(10 * (attempt + 1))

    raise RuntimeError("Gemini could not generate the story.")

if __name__ == "__main__":
    story = generate_story()

    os.makedirs("stories", exist_ok=True)

    filename = f"stories/story_{int(time.time())}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(story)

    print(f"Story saved successfully: {filename}")
