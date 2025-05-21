import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Telegram bot token
TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Web scraping fonksiyonu
def scrape_trendyol(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.trendyol.com/sr?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div.p-card-wrppr")
    results = []

    for product in products[:5]:
        try:
            name = product.select_one("div.product-down h3").get_text(strip=True)
            price = product.select_one("div.current-price__current").get_text(strip=True)
            link = "https://www.trendyol.com" + product.find("a")["href"]
            results.append(f"{name}\nFiyat: {price}\n{link}")
        except Exception:
            continue

    return results

# Telegram mesajlarına cevap
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = scrape_trendyol(query)

    if results:
        for item in results:
            await update.message.reply_text(item)
    else:
        await update.message.reply_text("Üzgünüm, ürün bulunamadı. Başka bir ürün deneyin.")

# Botu başlat
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
