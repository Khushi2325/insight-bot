import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from urllib.parse import urlencode

# 🔐 Get bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🌐 Your deployed website URL
BASE_URL = "https://pathly-labs-insight.onrender.com"


# ─────────────────────────────
# /start command
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 <b>Pathly Labs — Market Insight</b>\n\n"
        "Send a stock symbol like:\n"
        "<b>TCS</b>, <b>INFY</b>, <b>RELIANCE</b>\n\n"
        "<i>Educational market insights only.</i>",
        parse_mode="HTML"
    )


# ─────────────────────────────
# Handle stock messages
# ─────────────────────────────
async def handle_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        return

    # Normalize input
    symbol_raw = text.upper().replace(" ", "")

    # Remove .NS if user typed it
    if symbol_raw.endswith(".NS"):
        symbol_raw = symbol_raw[:-3]

    # Validate input
    if not symbol_raw.isalpha():
        await update.message.reply_text(
            "❌ Please send a valid NSE stock symbol.\n"
            "Example: TCS, INFY, RELIANCE"
        )
        return

    # Always append .NS
    symbol = symbol_raw + ".NS"

    # Build website link
    query = urlencode({"symbol": symbol})
    url = f"{BASE_URL}/search?{query}"

    # Reply message (Telegram-safe HTML)
    message = (
        f"📊 <b>{symbol_raw}</b> — Market Snapshot\n\n"
        "🔍 <b>View detailed charts & indicators:</b>\n"
        f"👉 <a href='{url}'>{url}</a>\n\n"
        "<i>Educational market insights only.</i>"
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        disable_web_page_preview=False
    )


# ─────────────────────────────
# Main runner
# ─────────────────────────────
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stock))

    print("🤖 Pathly Labs Telegram Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
