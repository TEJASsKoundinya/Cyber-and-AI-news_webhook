import os
import requests
import feedparser
from datetime import datetime, timedelta
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def get_google_news(query, max_results=10):
    """Fetch recent news from Google News RSS based on a query."""
    # when:1d ensures we only get news from the last 24 hours
    encoded_query = urllib.parse.quote(f"{query} when:1d")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    entries = feed.entries[:max_results]
    
    results = []
    for entry in entries:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return results

def get_arxiv_papers(max_results=5):
    """Fetch the latest AI whitepapers from arXiv."""
    url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    feed = feedparser.parse(url)
    results = []
    # Filter for the last 24 hours
    from datetime import timezone
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    
    for entry in feed.entries:
        try:
            # arXiv time format: 2026-07-02T18:00:00Z
            published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if published_date >= one_day_ago:
                results.append({
                    "title": entry.title.replace('\n', ' '),
                    "link": entry.link,
                    "published": entry.published
                })
        except ValueError:
            pass
            
    return results

def send_to_discord(title, items, webhook_url):
    """Send an embedded message to a Discord webhook."""
    if not items:
        content = f"No new updates for **{title}** in the last 24 hours."
        payload = {"content": content}
    else:
        embeds = []
        for i, item in enumerate(items):
            embed = {
                "title": item['title'],
                "url": item['link'],
                "description": f"Published: {item['published']}",
                "color": 3447003 # Blue
            }
            embeds.append(embed)
            
            # Discord allows max 10 embeds per message.
            if len(embeds) == 10 or i == len(items) - 1:
                payload = {
                    "content": f"## {title} (Last 24 Hours)\nHere are the top updates:",
                    "embeds": embeds
                }
                requests.post(webhook_url, json=payload)
                embeds = [] # reset for next batch if needed
                return # Only send max 10 to keep it as "Top 10"

    requests.post(webhook_url, json=payload)

def main():
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "your_webhook_url_here":
        print("Error: Please set DISCORD_WEBHOOK_URL in your .env file.")
        return

    print("Fetching Cybersecurity news...")
    cybersecurity_news = get_google_news("Cybersecurity", max_results=10)
    
    print("Fetching Identity and Access Management news...")
    iam_news = get_google_news("Identity and Access Management", max_results=10)
    
    print("Fetching AI news...")
    ai_news = get_google_news("Artificial Intelligence", max_results=10)
    
    print("Fetching AI papers from arXiv...")
    ai_papers = get_arxiv_papers(max_results=5)

    print("Sending updates to Discord...")
    send_to_discord("Top 10 Cybersecurity News", cybersecurity_news, DISCORD_WEBHOOK_URL)
    send_to_discord("Top 10 Identity and Access Management News", iam_news, DISCORD_WEBHOOK_URL)
    send_to_discord("Major AI News", ai_news, DISCORD_WEBHOOK_URL)
    send_to_discord("New AI Whitepapers (arXiv)", ai_papers, DISCORD_WEBHOOK_URL)
    
    print("Automation complete.")

if __name__ == "__main__":
    main()
