# 🎯 Quick Reference Card

## Setup (One-Time, 10 minutes)

### 1️⃣ Create Telegram Bot
- Open Telegram
- Search `@BotFather`
- Send `/newbot`
- Copy your **TOKEN**

### 2️⃣ Deploy (Pick One)
**Render.com** (Easiest)
- Sign up at render.com
- New Web Service
- Connect GitHub repo with the bot files
- Add env var: `TELEGRAM_BOT_TOKEN = [your token]`
- Deploy ✅

**Railway.app** (Also Easy)
- Sign up at railway.app
- New Project → Deploy from GitHub
- Add `TELEGRAM_BOT_TOKEN` env var
- Deploy ✅

### 3️⃣ Start Using
- Open Telegram
- Search your bot username
- Send `/start`
- Done! 🎉

---

## Commands (Use Anytime)

```
/track              → Add companies to track
/untrack            → Remove companies
/mycompanies        → See your tracked list
/search TICKER      → Find a company (e.g., /search INFY)
/latest             → Last 10 results filed
/upcoming           → Upcoming announcements (7 days)
/help               → Full help menu
```

---

## Examples

**Track Infosys:**
```
/search INFY
→ Click "Track This Company"
```

**Track Multiple Companies:**
```
/track
→ Click "Popular Companies"
→ Add INFY, TCS, RELIANCE, etc.
```

**View What You're Tracking:**
```
/mycompanies
→ Shows all tickers
```

**Stop Tracking:**
```
/untrack
→ Click company to remove
```

---

## How It Works

✅ You track companies → Bot checks every 4 hours → Instant Telegram notification when they file results

✅ Covers all 1000+ NSE/BSE listed companies

✅ Real-time data from official filings

✅ No manual checking needed

---

## Files to Upload to GitHub

```
your-repo/
├── earnings_bot.py          ← Main bot code
├── requirements.txt         ← Python dependencies
├── Procfile                 ← Deployment config
└── README.md               ← Your repo description
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Bot not responding | Send `/start` first, then wait 30 sec |
| No notifications | Check /mycompanies has companies, wait up to 4 hours |
| Deployment fails | Check bot token is set in environment variables |
| API error | Try `/help` or wait 5 min, earnings.thecore.in may be updating |

---

## Environment Variables

Only one needed:
```
TELEGRAM_BOT_TOKEN = 123456789:ABCdefGHIjklmnoPQRstUVwxyz
```

(Get this from @BotFather in Telegram)

---

## Customization (Optional)

Edit `earnings_bot.py` to:

1. **Check more/less frequently:**
   - Line with `interval=14400`
   - 3600 = every hour
   - 7200 = every 2 hours
   - 14400 = every 4 hours (default)

2. **Add more popular companies:**
   - Find `popular = [...]` line
   - Add tickers

3. **Change notification message:**
   - Edit message template in bot code

---

## Need Help?

1. Check `/help` in the bot
2. Re-read BOT_SETUP_GUIDE.md
3. Verify environment variables are set
4. Restart deployment service
5. Check internet connection

---

**Ready?** Start with Step 1 above! 🚀
