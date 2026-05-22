#!/usr/bin/env python3
"""
NSE/BSE Quarterly Results Telegram Bot
Tracks all listed companies for quarterly and annual earnings announcements
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)
from telegram.error import TelegramError
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
EARNINGS_API = "https://earnings.thecore.in/api"
USER_DATA_FILE = "user_data.json"
SELECTING_ACTION = 1
SELECTING_COMPANY = 2

class EarningsBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.application = Application.builder().token(bot_token).build()
        self.user_data = self.load_user_data()
        self.setup_handlers()

    def load_user_data(self) -> Dict:
        """Load user tracking preferences from file"""
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_user_data(self):
        """Save user tracking preferences"""
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(self.user_data, f, indent=2)

    def setup_handlers(self):
        """Setup all command handlers"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("track", self.track_menu))
        self.application.add_handler(CommandHandler("untrack", self.untrack_menu))
        self.application.add_handler(CommandHandler("mycompanies", self.list_tracked))
        self.application.add_handler(CommandHandler("latest", self.latest_results))
        self.application.add_handler(CommandHandler("upcoming", self.upcoming_results))
        self.application.add_handler(CommandHandler("search", self.search_company))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command - welcome message"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "tracked_companies": [],
                "notification_enabled": True,
                "created_at": datetime.now().isoformat()
            }
            self.save_user_data()

        welcome_text = """
🚀 *NSE/BSE Quarterly Results Tracker*

Get instant Telegram notifications whenever any listed company posts its quarterly or annual results!

*Available Commands:*
• /track - Add companies to track
• /untrack - Remove companies from tracking
• /mycompanies - View your tracked companies
• /latest - See latest results filed
• /upcoming - View upcoming result announcements
• /search TICKER - Search for a specific company
• /help - Show full help menu

*How it works:*
1. Use /track to add NSE/BSE listed companies
2. You'll get instant notifications when they file results
3. Results are checked every 4 hours for updates
4. No manual checking needed!

Let's get started! Use /track to add your first company. 👇
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
• Updated every 4 hours
• Covers 1000+ listed companies

*Privacy:*
• Your tracked companies are stored securely
• You can manage them anytime with /mycompanies
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def track_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    async def latest_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show latest quarterly results"""
        try:
            # Fetch from earnings API
            response = requests.get(f"{EARNINGS_API}/latest", timeout=5)
            if response.status_code == 200:
                results = response.json()[:10]  # Get latest 10
                
                if not results:
                    await update.message.reply_text("No recent results found.")
                    return

                message = "*📊 Latest Quarterly Results*\n\n"
                for i, result in enumerate(results, 1):
                    ticker = result.get('ticker', 'N/A')
                    company = result.get('company_name', 'Unknown')
                    date = result.get('filing_date', 'N/A')
                    revenue = result.get('revenue', 'N/A')
                    profit = result.get('net_profit', 'N/A')
                    
                    message += f"{i}. *{ticker}* - {company}\n"
                    message += f"   📅 {date}\n"
                    message += f"   💰 Revenue: {revenue} | Profit: {profit}\n\n"

                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("Unable to fetch latest results. Try again later.")
        except Exception as e:
            logger.error(f"Error fetching latest results: {e}")
            await update.message.reply_text("Error fetching results. Please try again.")

    async def upcoming_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    async def search_company(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                message += f"📈 Exchange: {company.get('exchange', 'N/A')}\n"
                message += f"💼 Status: {company.get('status', 'Active')}\n\n"
                
                latest = company.get('latest_result', {})
                if latest:
                    message += f"*Latest Results:*\n"
                    message += f"📅 Date: {latest.get('date', 'N/A')}\n"
                    message += f"💰 Revenue: {latest.get('revenue', 'N/A')}\n"
                    message += f"📊 Profit: {latest.get('profit', 'N/A')}\n"

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

    async def list_tracked(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List user's tracked companies"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.user_data:
            await update.message.reply_text("You haven't tracked any companies yet. Use /track to get started!")
            return

        tracked = self.user_data[user_id].get('tracked_companies', [])
        
        if not tracked:
            await update.message.reply_text("You haven't tracked any companies yet. Use /track to get started!")
            return

        message = f"*📊 Your Tracked Companies ({len(tracked)}):*\n\n"
        for ticker in tracked:
            message += f"• {ticker}\n"

        message += f"\n_Use /untrack to remove a company._"
        
        await update.message.reply_text(message, parse_mode='Markdown')

    async def untrack_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show untrack menu"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.user_data:
            await update.message.reply_text("You haven't tracked any companies yet.")
            return

        tracked = self.user_data[user_id].get('tracked_companies', [])
        
        if not tracked:
            await update.message.reply_text("You haven't tracked any companies yet.")
            return

        keyboard = []
        for ticker in tracked[:20]:  # Limit to 20 buttons
            keyboard.append([
                InlineKeyboardButton(f"❌ {ticker}", callback_data=f"remove_{ticker}")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Select a company to stop tracking:",
            reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        user_id = str(query.from_user.id)
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
            if user_id not in self.user_data:
                self.user_data[user_id] = {
                    "tracked_companies": [],
                    "notification_enabled": True,
                }
            
            if ticker not in self.user_data[user_id]["tracked_companies"]:
                self.user_data[user_id]["tracked_companies"].append(ticker)
                self.save_user_data()
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
            if user_id in self.user_data:
                if ticker in self.user_data[user_id]["tracked_companies"]:
                    self.user_data[user_id]["tracked_companies"].remove(ticker)
                    self.save_user_data()
                    await query.edit_message_text(
                        text=f"✅ Stopped tracking *{ticker}*",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text(
                        text=f"ℹ️ You weren't tracking {ticker}"
                    )

    async def send_notification(self, user_id: str, message: str):
        """Send notification to user"""
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
        except TelegramError as e:
            logger.error(f"Failed to send notification to {user_id}: {e}")

    async def check_and_notify(self, context: ContextTypes.DEFAULT_TYPE):
        """Background job to check for new results and notify users"""
        try:
            response = requests.get(f"{EARNINGS_API}/latest", timeout=5)
            if response.status_code == 200:
                latest_results = response.json()
                
                for user_id, user_prefs in self.user_data.items():
                    if not user_prefs.get('notification_enabled', True):
                        continue
                    
                    tracked = user_prefs.get('tracked_companies', [])
                    
                    for result in latest_results[:20]:  # Check latest 20
                        ticker = result.get('ticker', '')
                        
                        if ticker in tracked:
                            message = f"""
🎉 *{ticker}* filed quarterly results!

*Company:* {result.get('company_name', 'N/A')}
*Filing Date:* {result.get('filing_date', 'N/A')}
*Revenue:* {result.get('revenue', 'N/A')}
*Net Profit:* {result.get('net_profit', 'N/A')}

📈 Use /latest to see more details
                            """
                            
                            await self.send_notification(user_id, message)
        except Exception as e:
            logger.error(f"Error in background notification check: {e}")

    def run(self):
        """Run the bot"""
        # Add background job to check for results every 4 hours
        self.application.job_queue.run_repeating(
            self.check_and_notify,
            interval=14400,  # 4 hours in seconds
            first=60  # Start after 1 minute
        )
        
        logger.info("Starting bot...")
        self.application.run_polling()


def main():
    """Main entry point"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    bot = EarningsBot(token)
    bot.run()


if __name__ == '__main__':
    main()
