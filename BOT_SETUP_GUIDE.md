# 🚀 NSE/BSE Quarterly Results Telegram Bot - Setup Guide

## Overview
This bot tracks all NSE/BSE listed companies and sends you Telegram notifications whenever they file quarterly or annual results. It runs 24/7 on free infrastructure.

---

## Step 1: Create Your Telegram Bot (5 minutes)

1. **Open Telegram** on your phone/computer
2. **Search for** `@BotFather` and click to open
3. **Send** `/newbot`
4. **Choose a name** for your bot (e.g., "My Earnings Bot")
5. **Choose a username** (must end with "bot", e.g., "my_earnings_bot")
6. **Copy the TOKEN** that BotFather gives you (looks like: `123456789:ABCDefGHIjklmnoPQRstUVwxYZ`)
7. **Save this token** - you'll need it in Step 3

---

## Step 2: Deploy to Free Hosting (Choose One)

### **Option A: Render.com (Recommended - Easiest)**

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. **Connect your GitHub account** (or use GitHub web editor)
4. In the GitHub web editor, create a new repo or use this structure:
   ```
   your-repo/
   ├── earnings_bot.py
   ├── requirements.txt
   └── Procfile
   ```
5. **Create Procfile** with this content:
   ```
   web: python earnings_bot.py
   ```
6. Push to GitHub
7. In Render, select the repo and set:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python earnings_bot.py`
8. **Add environment variable:**
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: [Paste your token from Step 1]
9. Click **"Deploy"** - done! ✅

### **Option B: Railway.app (Very Simple)**

1. Go to [railway.app](https://railway.app) and sign up (free)
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Connect your GitHub account
4. Select your repo with the bot files
5. Railway auto-detects Python. Set environment variable:
   - `TELEGRAM_BOT_TOKEN = [Your token]`
6. Deploy - done! ✅

### **Option C: Heroku (Legacy but Works)**

1. Go to [heroku.com](https://heroku.com) and sign up
2. Create a new app
3. Connect your GitHub repo
4. Add buildpack: `heroku/python`
5. Set `TELEGRAM_BOT_TOKEN` config var
6. Deploy

---

## Step 3: Get Bot Running Locally (Testing)

If you want to test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your bot token
export TELEGRAM_BOT_TOKEN="your_token_here"

# Run the bot
python earnings_bot.py
```

---

## Step 4: Start Using Your Bot

1. **Open Telegram** on your phone
2. **Search for your bot** by the username you created (e.g., `@my_earnings_bot`)
3. **Click** to open the bot chat
4. **Send** `/start` to initialize
5. **Use commands:**

### Available Commands:

| Command | What It Does |
|---------|-------------|
| `/track` | Browse and add companies to track |
| `/untrack` | Remove companies from tracking |
| `/mycompanies` | List all your tracked companies |
| `/latest` | See latest 10 results filed |
| `/upcoming` | View upcoming result announcements |
| `/search TICKER` | Search for a company (e.g., `/search INFY`) |
| `/help` | Show full help menu |

---

## Examples

### Track Companies
```
/track
→ Click "Popular Companies"
→ Select INFY, TCS, RELIANCE, etc.
```

### Search for a Company
```
/search HDFC
→ Bot shows HDFC details
→ Click "Track This Company"
```

### View Your Tracked List
```
/mycompanies
→ Shows all companies you're tracking
```

### Remove a Company
```
/untrack
→ Click company name to remove
```

---

## How Notifications Work

- **Frequency:** Bot checks for new results every 4 hours
- **Coverage:** All 1000+ NSE/BSE listed companies
- **Instant:** You get a Telegram notification immediately when a tracked company files results
- **Details:** Notifications include company name, filing date, revenue, and net profit

---

## Data Source

The bot uses **earnings.thecore.in** API which provides:
- Real-time NSE/BSE filing data
- 1000+ listed companies
- Updated every 2 hours during trading day
- Free access, no authentication needed

---

## Troubleshooting

### Bot doesn't respond to /start
- Make sure you've started the bot (sent `/start`)
- Restart the deployment (Render/Railway dashboard)
- Check environment variable is set correctly

### Not receiving notifications
- Verify company is in your /mycompanies list
- Check that notifications are enabled in settings
- Wait up to 4 hours for the next check cycle

### Need to update bot code
- Edit earnings_bot.py in your GitHub repo
- Render/Railway auto-deploys changes
- Restart the service if needed

### API returns no data
- earnings.thecore.in might be down temporarily
- Try /latest or /upcoming in 5 minutes
- Check their status at earnings.thecore.in

---

## Advanced: Customize the Bot

Edit `earnings_bot.py` to:

1. **Change check frequency:**
   ```python
   interval=14400,  # Change to 3600 for hourly, 7200 for 2 hours
   ```

2. **Add more popular companies:**
   ```python
   popular = ["INFY", "TCS", "RELIANCE", "HDFC", ...]
   ```

3. **Customize notification message:**
   Edit the notification template in `send_notification()` method

---

## Security & Privacy

- Your bot token is stored as an environment variable (never in code)
- User data (tracked companies) stored locally in `user_data.json`
- No personal information collected beyond your Telegram user ID
- You control what companies are tracked

---

## Support & Updates

If earnings.thecore.in API changes, update the API endpoints in:
- Line ~35: `EARNINGS_API = "https://earnings.thecore.in/api"`

Alternative data sources:
- NSE Official API: `https://www.nseindia.com/`
- BSE Data API: `https://www.bseindia.com/`

---

## Next Steps

1. ✅ Create bot with BotFather
2. ✅ Deploy to Render/Railway
3. ✅ Open bot in Telegram
4. ✅ Use /track to add companies
5. ✅ Enjoy notifications! 🎉

---

**Questions?** Check the `/help` command in the bot or edit the code to add more features!
