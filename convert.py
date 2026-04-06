import json
import re, sys
from collections import Counter
import emoji

def extract_emojis(text):
    return [e['emoji'] for e in emoji.emoji_list(text)]

src = sys.argv[1]

CHANNEL = "xorping"

with open(src, "r", encoding="utf-8") as f:
    data = json.load(f)

posts = []
emoji_counter = Counter()

for msg in data["messages"]:
    if msg.get("type") != "message":
        continue

    text = msg.get("text", "")

    if isinstance(text, list):
        text = "".join(
            part if isinstance(part, str) else part.get("text", "")
            for part in text
        )

    if not text.strip():
        continue

    emojis = extract_emojis(text)

    for e in emojis:
        emoji_counter[e] += 1

    posts.append({
        "id": msg["id"],
        "date": msg["date"][:10],
        "text": text,
        "emojis": emojis,
        "url": f"https://t.me/{CHANNEL}/{msg['id']}"
    })

# ---- create emoji metadata ----

emoji_stats = []
max_freq = max(emoji_counter.values(), default=1)

for emoji, count in emoji_counter.items():
    ratio = count / max_freq

    if ratio > 0.66:
        size = "large"
    elif ratio > 0.33:
        size = "medium"
    else:
        size = "small"

    emoji_stats.append({
        "emoji": emoji,
        "count": count,
        "size": size
    })

# sort by frequency DESC
emoji_stats.sort(key=lambda x: x["count"], reverse=True)

# ---- final output ----

output = {
    "posts": posts,
    "emojis": emoji_stats
}

with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Done")
