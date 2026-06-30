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
          # 🧠 AI / LLM / ML
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "llm",
    "large language model",
    "gpt",
    "openai",
    "chatgpt",
    "claude",
    "gemini",
    "anthropic",
    "microsoft copilot",
    "google ai",
    "meta ai",

    # ⚙️ SAP / ERP
    "sap",
    "s/4hana",
    "s4hana",
    "sap fi",
    "sap mm",
    "sap sd",
    "sap abap",
    "abap",
    "fico",
    "sap erp",
    "erp",
    "sap consultant",
    "sap transformation",
    "sap migration",
    "rise with sap",

    # ☁️ Enterprise / Cloud / Dev
    "cloud",
    "azure",
    "aws",
    "google cloud",
    "kubernetes",
    "microservices",
    "devops",
    "data engineering",
    "data platform",
    "enterprise software",
    "digital transformation",
    "automation"
]

FEEDS = [
    # 🧠 AI & Machine Learning
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/artificial-intelligence/rss/index.xml",

    # 🧠 Google AI News (güçlü genel AI feed)
    "https://news.google.com/rss/search?q=artificial+intelligence+OR+LLM+OR+GPT+OR+machine+learning&hl=en-US&gl=US&ceid=US:en",

    # 💼 SAP & Enterprise Systems
    "https://news.google.com/rss/search?q=SAP+S%2F4HANA+OR+SAP+FI+OR+SAP+MM+OR+SAP+SD&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=ERP+transformation+OR+enterprise+software+OR+SAP+consultant&hl=en-US&gl=US&ceid=US:en",

    # ⚙️ General enterprise tech (Microsoft, Google, cloud, etc.)
    "https://news.google.com/rss/search?q=cloud+computing+OR+Azure+OR+AWS+OR+Google+Cloud+enterprise&hl=en-US&gl=US&ceid=US:en"
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

MAX_NEWS = 10

if new_jobs:
    message = (
        f"🤖 AI & SAP Daily Update\n"
        f"Toplam eşleşme: {len(new_jobs)}\n"
        f"İlk {min(MAX_NEWS, len(new_jobs))} haber:\n\n"
        + "\n\n".join(new_jobs[:MAX_NEWS])
    )
    send(message)
else:
    print("NO MATCHING NEWS FOUND")
          

save_seen(seen)
send("✅ Test: Workflow başarıyla çalıştı.")
print("🔥 SCRIPT FINISHED")
