import os
from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

from crypto_data import get_crypto_list, get_crypto_price
from currency_list import get_currency_list
from currency_convert import currency_converter

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

ASK_CRYPTO = 1
ASK_CURRENCY = 2

LIST_LIMIT = 20


MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["📋 Crypto list"],
        ["💱 Currency list"],
        ["💰 Check price"],
    ],
    resize_keyboard=True
)

MORE_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("➡️ More", callback_data="more")]
    ]
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''🚀 Welcome to Crypto Price Bot 👋

This bot helps you check live crypto prices in different currencies 💰

Here’s how to use it:

📋 **Crypto list**
View available cryptocurrencies and their symbols
Example: Bitcoin → BTC

💱 **Currency list**
View supported currency symbols
Example: US Dollar → USD, Euro → EUR

💰 **Check price**

1. Send a crypto symbol (BTC, ETH, SOL...)
2. Then send a currency symbol (USD, EUR, GBP...)
3. The bot will instantly convert the crypto price for you ⚡

❗ Important:
Please use SYMBOLS only, not full names.
✅ BTC
❌ Bitcoin

If you don’t know the symbols, check the Crypto list or Currency list first 😊
''',
        reply_markup=MAIN_MENU
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "📋 Crypto list":
        context.user_data["list_type"] = "crypto"
        context.user_data["list_index"] = 0

        crypto_text = get_crypto_list(start=0, limit=LIST_LIMIT)

        await update.message.reply_text(
            crypto_text,
            reply_markup=MORE_KEYBOARD
        )

        return ConversationHandler.END

    if text == "💱 Currency list":
        context.user_data["list_type"] = "currency"
        context.user_data["list_index"] = 0

        currency_text = get_currency_list(start=0, limit=LIST_LIMIT)

        await update.message.reply_text(
            currency_text,
            reply_markup=MORE_KEYBOARD
        )

        return ConversationHandler.END

    if text == "💰 Check price":
        await update.message.reply_text(
            "Send me the crypto symbol, e.g. BTC, ETH, SOL."
        )

        return ASK_CRYPTO

    await update.message.reply_text(
        "Please choose one of the menu buttons 👇",
        reply_markup=MAIN_MENU
    )

    return ConversationHandler.END


async def more_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    list_type = context.user_data.get("list_type")
    current_index = context.user_data.get("list_index", 0)

    next_index = current_index + LIST_LIMIT
    context.user_data["list_index"] = next_index

    if list_type == "crypto":
        result_text = get_crypto_list(start=next_index, limit=LIST_LIMIT)

    elif list_type == "currency":
        result_text = get_currency_list(start=next_index, limit=LIST_LIMIT)

    else:
        await query.message.reply_text(
            "Please choose Crypto list or Currency list first 👇",
            reply_markup=MAIN_MENU
        )
        return

    if not result_text:
        await query.message.reply_text(
            "No more items 😅",
            reply_markup=MAIN_MENU
        )
        return

    await query.message.reply_text(
        result_text,
        reply_markup=MORE_KEYBOARD
    )


async def handle_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip().upper()

    price = get_crypto_price(symbol)

    if price is None:
        await update.message.reply_text(
            f"❌ I couldn't find {symbol}.\nTry something like BTC, ETH, SOL.",
            reply_markup=MAIN_MENU
        )

        return ConversationHandler.END

    context.user_data["symbol"] = symbol
    context.user_data["price"] = price

    await update.message.reply_text(
        "Now send me the currency symbol, e.g. USD, EUR, GBP."
    )

    return ASK_CURRENCY


async def handle_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = update.message.text.strip().upper()

    symbol = context.user_data["symbol"]
    price = context.user_data["price"]

    convert = float(currency_converter('USD', currency))
    result = convert * price
    await update.message.reply_text(
        f"💰 {symbol} price: {result:,.2f} {currency}",
        reply_markup=MAIN_MENU
    )

    context.user_data.clear()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "Cancelled.",
        reply_markup=MAIN_MENU
    )

    return ConversationHandler.END


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)
        ],
        states={
            ASK_CRYPTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_crypto)
            ],
            ASK_CURRENCY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(more_button_handler, pattern="more"))
    app.add_handler(conversation_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()