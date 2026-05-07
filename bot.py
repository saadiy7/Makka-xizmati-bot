import os
import logging
import requests
from groq import Groq

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def get_ai_reply(message):
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Siz yordamchi botsiz. O'zbek tilida javob bering."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def main():
    offset = 0
    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
        response = requests.get(url, timeout=35)
        updates = response.json().get("result", [])
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")
            if text and chat_id:
                reply = get_ai_reply(text)
                send_message(chat_id, reply)

if __name__ == "__main__":
    main()
