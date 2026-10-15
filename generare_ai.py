import requests
import json
import time

API_KEY = "sk-f868d5011ad54595989cd87cb59fa417"
URL = "https://api.deepseek.com/chat/completions"

def genereaza_quiz(topic, retries=3):
    prompt = f"""
    Creează un quiz de exact 10 întrebări despre topicul: {topic}.
    Întoarce STRICT un JSON în formatul:
    [
      {{
        "intrebare": "...",
        "variante": {{"a":"...", "b":"...", "c":"...", "d":"..."}},
        "corect": "a"
      }}
    ]
    FĂRĂ TEXT ÎN PLUS.
    """

    for i in range(retries):
        try:
            r = requests.post(
                URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )

            data = r.json()
            raspuns = data["choices"][0]["message"]["content"]
            return json.loads(raspuns)

        except Exception:
            time.sleep(1)

    return None
