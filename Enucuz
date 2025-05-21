from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"

fake_prices = {
    "iphone": {"Trendyol": 72000, "Hepsiburada": 71000, "Amazon": 73000},
    "samsung televizyon": {"Trendyol": 10000, "Hepsiburada": 9500, "Amazon": 10200},
    "airfryer": {"Trendyol": 1250, "Hepsiburada": 1199, "Amazon": 1300},
}

def find_cheapest(prices):
    cheapest_store = min(prices, key=prices.get)
    cheapest_price = prices[cheapest_store]
    return cheapest_store, cheapest_price

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ürün adını yaz, en ucuz fiyatı bulayım.\nÖrnek: iPhone, Samsung Televizyon, Airfryer"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    found = False
    for key in fake_prices.keys():
        if key in user_text:
            prices = fake_prices[key]
            cheapest_store, cheapest_price = find_cheapest(prices)

            response = f"{key.title()} fiyatları:\n"
            for store, price in prices.items():
                response += f"- {store}: {price} TL\n"
            response += f"→ En ucuz: {cheapest_store} ({cheapest_price} TL) (Satın Al)"

            await update.message.reply_text(response)
            found = True
            break

    if not found:
        await update.message.reply_text("Üzgünüm, bu ürün için veri yok. Başka ürün deneyin.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
