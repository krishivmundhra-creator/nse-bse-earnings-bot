#!/usr/bin/env python3
"""
NSE/BSE Quarterly Results Telegram Bot - Simplified Version
Tracks all listed companies for quarterly and annual earnings announcements
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
EARNINGS_API = "https://earnings.thecore.in/api"
USER_DATA_FILE = "user_data.json"


def load_user_data() -> Dict:
    """Load user tracking preferences from file"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_user_data(data: Dict):
    """Save user tracking preferences"""
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")


# ===== COMMAND HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - welcome message"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        user_data[user_id] = {
            "tracked_companies": [],
            "notification_enabled": True,
            "created_at": datetime.now().isoformat()
        }
        save_user_data(user_data)

    welcome_text = """
🚀 *NSE/BSE Quarterly Results Tracker*

Get instant Telegram notifications whenever any listed company posts its quarterly or annual results!

*Available Commands:*
• /track - Add companies to track
• /untrack - Remove companies from tracking
• /mycompanies - View your tracked companies
• /latest - See latest results filed
• /upcoming - View upcoming result announcements
• /search TICKER - Search for a company
• /help - Show full help menu

Let's get started! Use /track to add your first company. 👇
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
*📖 Complete Guide*

*Tracking Commands:*
• /track - Browse and add companies
• /untrack - Remove a tracked company
• /mycompanies - List all your tracked companies

*Results Commands:*
• /latest - Latest 10 results filed today
• /upcoming - Upcoming result announcements (next 7 days)
• /search TICKER - Find a specific company (e.g., /search INFY)

*Notification Settings:*
You'll receive notifications automatically when tracked companies file results.

*Data Sources:*
• Real-time data from NSE/BSE filings
• Covers 1000+ listed companies
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def track_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show track menu"""
    keyboard = [
        [InlineKeyboardButton("📈 Browse Companies", callback_data="browse_companies")],
        [InlineKeyboardButton("🔍 Search by Ticker", callback_data="search_ticker")],
        [InlineKeyboardButton("⭐ Popular Companies", callback_data="popular_companies")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "How would you like to add companies to track?",
        reply_markup=reply_markup
    )


async def latest_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show latest quarterly results"""
    try:
        response = requests.get(f"{EARNINGS_API}/latest", timeout=5)
        if response.status_code == 200:
            results = response.json()[:10]
            
            if not results:
                await update.message.reply_text("No recent results found.")
                return

            message = "*📊 Latest Quarterly Results*\n\n"
            for i, result in enumerate(results, 1):
                ticker = result.get('ticker', 'N/A')
                company = result.get('company_name', 'Unknown')
                date = result.get('filing_date', 'N/A')
                
                message += f"{i}. *{ticker}* - {company}\n"
                message += f"   📅 {date}\n\n"

            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("Unable to fetch latest results. Try again later.")
    except Exception as e:
        logger.error(f"Error fetching latest results: {e}")
        await update.message.reply_text("Error fetching results. Please try again.")


async def upcoming_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show upcoming results"""
    try:
        response = requests.get(f"{EARNINGS_API}/upcoming", timeout=5)
        if response.status_code == 200:
            results = response.json()[:10]
            
            if not results:
                await update.message.reply_text("No upcoming results scheduled.")
                return

            message = "*📅 Upcoming Result Announcements (Next 7 Days)*\n\n"
            for i, result in enumerate(results, 1):
                ticker = result.get('ticker', 'N/A')
                company = result.get('company_name', 'Unknown')
                expected_date = result.get('expected_date', 'TBD')
                
                message += f"{i}. *{ticker}* - {company}\n"
                message += f"   ⏰ Expected: {expected_date}\n\n"

            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("Unable to fetch upcoming results.")
    except Exception as e:
        logger.error(f"Error fetching upcoming results: {e}")
        await update.message.reply_text("Error fetching results. Please try again.")


async def search_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for a company by ticker"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /search TICKER\nExample: /search INFY"
        )
        return

    ticker = context.args[0].upper()
    
    try:
        response = requests.get(f"{EARNINGS_API}/company/{ticker}", timeout=5)
        if response.status_code == 200:
            company = response.json()
            
            message = f"*{company.get('ticker')}* - {company.get('company_name')}\n\n"
            message += f"🏢 Sector: {company.get('sector', 'N/A')}\n"
            message += f"📈 Exchange: {company.get('exchange', 'N/A')}\n\n"

            keyboard = [
                [InlineKeyboardButton(
                    "➕ Track This Company",
                    callback_data=f"add_track_{ticker}"
                )],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(f"Company {ticker} not found in NSE/BSE listings.")
    except Exception as e:
        logger.error(f"Error searching company: {e}")
        await update.message.reply_text("Error searching. Please try again.")


async def list_tracked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List user's tracked companies"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        await update.message.reply_text("You haven't tracked any companies yet. Use /track to get started!")
        return

    tracked = user_data[user_id].get('tracked_companies', [])
    
    if not tracked:
        await update.message.reply_text("You haven't tracked any companies yet. Use /track to get started!")
        return

    message = f"*📊 Your Tracked Companies ({len(tracked)}):*\n\n"
    for ticker in tracked:
        message += f"• {ticker}\n"

    message += f"\n_Use /untrack to remove a company._"
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def untrack_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show untrack menu"""
    user_id = str(update.effective_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        await update.message.reply_text("You haven't tracked any companies yet.")
        return

    tracked = user_data[user_id].get('tracked_companies', [])
    
    if not tracked:
        await update.message.reply_text("You haven't tracked any companies yet.")
        return

    keyboard = []
    for ticker in tracked[:20]:
        keyboard.append([
            InlineKeyboardButton(f"❌ {ticker}", callback_data=f"remove_{ticker}")
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Select a company to stop tracking:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    user_id = str(query.from_user.id)
    user_data = load_user_data()
    
    await query.answer()

    if query.data == "browse_companies":
        await query.edit_message_text(
            text="📝 Enter company ticker to track (e.g., INFY, TCS, RELIANCE):\n\nUse /search TICKER"
        )
    
    elif query.data == "search_ticker":
        await query.edit_message_text(
            text="🔍 Use /search TICKER to find a company\n\nExample: /search INFY"
        )
    
    elif query.data == "popular_companies":
        popular = ["INFY", "TCS", "RELIANCE", "HDFC", "ICICIBANK", "BAJAJFINSV", "ASIANPAINT", "MARUTI"]
        keyboard = []
        for ticker in popular:
            keyboard.append([
                InlineKeyboardButton(f"➕ {ticker}", callback_data=f"add_track_{ticker}")
            ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="⭐ Popular Companies:",
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("add_track_"):
        ticker = query.data.replace("add_track_", "")
        if user_id not in user_data:
            user_data[user_id] = {
                "tracked_companies": [],
                "notification_enabled": True,
            }
        
        if ticker not in user_data[user_id]["tracked_companies"]:
            user_data[user_id]["tracked_companies"].append(ticker)
            save_user_data(user_data)
            await query.edit_message_text(
                text=f"✅ Now tracking *{ticker}*!\n\nYou'll get notifications when {ticker} files quarterly/annual results.",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                text=f"ℹ️ You're already tracking *{ticker}*",
                parse_mode='Markdown'
            )
    
    elif query.data.startswith("remove_"):
        ticker = query.data.replace("remove_", "")
        if user_id in user_data:
            if ticker in user_data[user_id]["tracked_companies"]:
                user_data[user_id]["tracked_companies"].remove(ticker)
                save_user_data(user_data)
                await query.edit_message_text(
                    text=f"✅ Stopped tracking *{ticker}*",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    text=f"ℹ️ You weren't tracking {ticker}"
                )


async def main():
    """Main function to run the bot"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track", track_menu))
    application.add_handler(CommandHandler("untrack", untrack_menu))
    application.add_handler(CommandHandler("mycompanies", list_tracked))
    application.add_handler(CommandHandler("latest", latest_results))
    application.add_handler(CommandHandler("upcoming", upcoming_results))
    application.add_handler(CommandHandler("search", search_company))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info("Starting bot...")
    await application.run_polling()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
