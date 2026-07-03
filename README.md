# Discord News Automation Bot

A scheduled automation script that fetches the latest news from the last 24 hours and securely posts it to a Discord webhook.

## Features

This bot automatically fetches and formats the top 10 most recent updates for:
- 🔒 **Cybersecurity** (via Google News RSS)
- 🔑 **Identity and Access Management** (via Google News RSS)
- 🤖 **Artificial Intelligence** (via Google News RSS)
- 📄 **New AI Whitepapers & Journals** (via arXiv API)

## Security

This repository is designed to be completely safe to deploy publicly. The Discord webhook URL is never hardcoded. Instead, it relies on environment variables (`.env` for local usage) and GitHub Secrets (`DISCORD_WEBHOOK_URL`) for cloud deployments, ensuring your Discord channel remains secure.

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd discord-news-bot
   ```

2. **Set up the Webhook URL:**
   Copy the example environment file and add your Discord webhook URL.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `your_webhook_url_here` with your actual Webhook URL.

3. **Install Dependencies:**
   Ensure you have Python 3 installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script manually:**
   ```bash
   python main.py
   ```

## Cloud Deployment (GitHub Actions)

This project includes a GitHub Actions workflow (`.github/workflows/schedule.yml`) that will automatically run the script every day at 08:00 UTC.

To enable it:
1. Push this repository to GitHub.
2. Go to your repository **Settings**.
3. Navigate to **Secrets and variables** -> **Actions**.
4. Click **New repository secret**.
5. Name the secret `DISCORD_WEBHOOK_URL` and paste your webhook URL as the value.

The bot is now fully deployed and will automatically post updates to your Discord server daily!
