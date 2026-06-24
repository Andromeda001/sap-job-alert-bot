print("🔥 SCRIPT STARTED")
import feedparser
import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT_TOKEN LOADED:", bool(BOT_TOKEN))
print("CHAT_ID LOADED:", bool(CHAT_ID))

KEYWORDS = [
    "SAP MM",
    "SAP S/4HANA",
    "SAP Consultant",
    "SAP Procurement",
    "SAP FI",
    "SAP SD",
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
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

    print("TELEGRAM STATUS:", r.status_code)
    print("TELEGRAM RESPONSE:", r.text)

def match(title):
    return any(k.lower() in title.lower() for k in KEYWORDS)

seen = load_seen()
new_jobs = []

for feed_url in FEEDS:
    print("CHECKING FEED:", feed_url)

    feed = feedparser.parse(feed_url)

    print("ENTRIES FOUND:", len(feed.entries))

    for entry in feed.entries[:20]:
        uid = entry.get("id", entry.get("link"))

        if uid in seen:
            continue

        print("JOB FOUND:", entry.title)

        if match(entry.title):
            print("MATCHED KEYWORD:", entry.title)
            new_jobs.append(f"📌 {entry.title}\n{entry.link}")

        seen.add(uid)

print("TOTAL NEW JOBS:", len(new_jobs))

if new_jobs:
    send("🔥 SAP Job Alert\n\n" + "\n\n".join(new_jobs))
else:
    print("NO MATCHING JOBS FOUND")

save_seen(seen)
print("🔥 SCRIPT FINISHED")
