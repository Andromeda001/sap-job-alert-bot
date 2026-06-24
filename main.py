import feedparser
import requests
import os
import json

BOT_TOKEN = os.getenv("8607950128:AAFyn2ocKMXisJYxgnhYYIJJ1sdAsdSLc8U")
CHAT_ID = os.getenv("7792691313")

KEYWORDS = [
    "SAP MM",
    "SAP S/4HANA",
    "SAP Consultant",
    "SAP Procurement",
    "SAP FI",
    "SAP SD"
]

FEEDS = [
    "https://remoteok.com/remote-sap-jobs.rss",
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",
]

STATE_FILE = "seen.json"

def load_seen():
    try:
        return set(json.load(open(STATE_FILE)))
    except:
        return set()

def save_seen(seen):
    json.dump(list(seen), open(STATE_FILE, "w"))

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def match(title):
    return any(k.lower() in title.lower() for k in KEYWORDS)

seen = load_seen()
new_jobs = []

for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:20]:
        uid = entry.get("id", entry.get("link"))

        if uid in seen:
            continue

        if match(entry.title):
            new_jobs.append(f"📌 {entry.title}\n{entry.link}")

        seen.add(uid)

if new_jobs:
    send("🔥 SAP Job Alert\n\n" + "\n\n".join(new_jobs))

save_seen(seen)
