import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

from crypto_price import crypto_price as get_crypto_price
from currency_convert import currency_converter

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

ASK_CURRENCY = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi 👋 Send me a crypto symbol like BTC, ETH, SOL."
    )


async def handle_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip().upper()

    price = get_crypto_price(symbol)

    if price is None:
        await update.message.reply_text(
            f"❌ I couldn't find {symbol}.\nTry something like BTC, ETH, SOL."
        )
        return ConversationHandler.END

    context.user_data["symbol"] = symbol
    context.user_data["price"] = price

    await update.message.reply_text(
        "In what currency do you want to see the price?\n"
        "Send me the symbol, e.g. USD, EUR, GBP."
    )

    return ASK_CURRENCY


async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = update.message.text.strip().upper()

    symbol = context.user_data["symbol"]
    price = context.user_data["price"]

    converted_price = float(currency_converter(symbol, currency))

    await update.message.reply_text(
    f"💰 {symbol} price: {converted_price:,.2f} {currency}"
)

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symbol)
        ],
        states={
            ASK_CURRENCY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conversation_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()