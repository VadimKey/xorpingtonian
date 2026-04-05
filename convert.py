import json, sys
import re
from datetime import datetime

EMOJI_REGEX = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF]+",
    flags=re.UNICODE
)

def extract_emojis(text):
    return EMOJI_REGEX.findall(text)

src = sys.argv[1]

with open(src, "r", encoding="utf-8") as f:
    data = json.load(f)

posts = []

for msg in data["messages"]:
    if msg.get("type") != "message":
        continue

    text = msg.get("text", "")

    # Telegram sometimes stores text as list (formatted)
    if isinstance(text, list):
        text = "".join(part if isinstance(part, str) else part.get("text", "") for part in text)

    emojis = extract_emojis(text)

    if not text.strip():
        continue

    posts.append({
        "id": msg["id"],
        "date": msg["date"][:10],  # YYYY-MM-DD
        "text": text,
        "emojis": emojis
    })

# sort newest first
posts.sort(key=lambda x: x["date"], reverse=True)

with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"Exported {len(posts)} posts")
