# 📊 NSE/BSE Quarterly Results Telegram Bot

Instant Telegram notifications for quarterly and annual results of **all NSE/BSE listed companies** — no manual checking needed.

## Features

✅ **Real-Time Notifications** — Get Telegram alerts the moment a tracked company files results  
✅ **1000+ Companies** — Track any NSE/BSE listed company  
✅ **Simple Commands** — `/track`, `/search`, `/latest`, `/upcoming`  
✅ **Always On** — Runs 24/7 on free cloud infrastructure  
✅ **Free** — No subscriptions or paid APIs required  
✅ **Smart Checking** — Checks every 4 hours during market hours  

## Quick Start

### 1. Create Telegram Bot
```bash
# Open Telegram
# Search @BotFather
# Send /newbot
# Copy your TOKEN
```

### 2. Deploy (2 minutes)

**Render.com:**
1. Sign up at render.com
2. New Web Service → Connect GitHub
3. Add environment variable: `TELEGRAM_BOT_TOKEN=[your token]`
4. Deploy ✅

**Or Railway.app:**
1. Sign up at railway.app
2. New Project → Deploy from GitHub
3. Add `TELEGRAM_BOT_TOKEN` env var
4. Deploy ✅

### 3. Start Using
```bash
# Open Telegram
# Search your bot
# Send /start
# Send /track to add companies
```

## Commands

| Command | Purpose |
|---------|---------|
| `/track` | Add companies to track |
| `/untrack` | Remove companies |
| `/mycompanies` | See your tracked list |
| `/search TICKER` | Find company by ticker (e.g., `/search INFY`) |
| `/latest` | View latest 10 results filed |
| `/upcoming` | View upcoming announcements (7 days) |
| `/help` | Show help menu |

## Examples

**Track Infosys:**
```
/search INFY
→ Click "Track This Company"
```

**Track Popular Companies:**
```
/track
→ Click "Popular Companies"
→ Select INFY, TCS, RELIANCE, etc.
```

**View Your Tracked Companies:**
```
/mycompanies
```

**Stop Tracking a Company:**
```
/untrack
→ Click company name
```

## How It Works

1. You track companies with `/track` or `/search`
2. Bot checks NSE/BSE filings every 4 hours
3. When a tracked company files results, you get instant Telegram notification
4. Notification includes: company, filing date, revenue, net profit

## Data Source

Uses **earnings.thecore.in** API:
- Real-time NSE/BSE filing data
- 1000+ listed companies covered
- Updated every 2 hours during market hours
- Free, no authentication needed

## Requirements

- Python 3.8+
- Telegram account
- Free cloud hosting (Render, Railway, or Heroku)

## Installation (Local Development)

```bash
# Clone repo
git clone https://github.com/yourusername/nse-bse-earnings-bot.git
cd nse-bse-earnings-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export TELEGRAM_BOT_TOKEN="your_token_here"

# Run bot
python earnings_bot.py
```

## File Structure

```
nse-bse-earnings-bot/
├── earnings_bot.py          # Main bot logic
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment config
├── BOT_SETUP_GUIDE.md      # Detailed setup guide
├── QUICK_START.md          # Quick reference
└── README.md               # This file
```

## Configuration

Only one environment variable needed:

```
TELEGRAM_BOT_TOKEN = your_bot_token_here
```

### Optional Customizations

Edit `earnings_bot.py`:

**Change check frequency** (default: every 4 hours):
```python
# Line ~245
interval=14400,  # 3600=1hr, 7200=2hrs, 14400=4hrs
```

**Add more popular companies:**
```python
# Line ~180 in button_callback
popular = ["INFY", "TCS", "RELIANCE", "HDFC", ...]
```

## Troubleshooting

**Bot not responding to /start:**
- Wait 30 seconds and try again
- Restart deployment service
- Check `TELEGRAM_BOT_TOKEN` is set correctly

**Not receiving notifications:**
- Verify company is in `/mycompanies`
- Wait up to 4 hours for next check cycle
- Check Telegram notification settings

**API errors:**
- earnings.thecore.in might be updating
- Try again in 5 minutes
- Check your internet connection

## Deployment Options

### Render.com (Recommended)
- Free tier available
- Auto-deploys on GitHub push
- Simple environment variable setup

### Railway.app
- Very straightforward setup
- Free monthly credits
- Automatic redeploy

### Heroku
- Classic option
- Free tier recently removed (paid)
- Still works if you add payment method

## Contributing

Found a bug or want to add features?
- Open an issue
- Submit a pull request
- Suggestions welcome!

## Roadmap

- [ ] Add sector-based filtering
- [ ] Add price alerts on results
- [ ] Add financial metrics comparison
- [ ] Add custom notification timing
- [ ] Web dashboard for tracking

## License

MIT License — Use freely!

## Support

**Issues?** Check the `/help` command in the bot or refer to `BOT_SETUP_GUIDE.md`

## Disclaimer

This bot uses publicly available NSE/BSE data. Not affiliated with NSE, BSE, or any company. Use at your own risk. Data is provided as-is without warranty.

---

**Made for Indian stock market enthusiasts by Krishiv** 📈
