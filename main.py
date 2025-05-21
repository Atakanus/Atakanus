import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Telegram bot token (güvenli şekilde saklamayı unutma)
BOT_TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"

# Logger kurulumu
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Trendyol'dan ürün arama fonksiyonu
def scrape_trendyol(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.trendyol.com/sr?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("li.product-item")
    results = []

    for product in products[:5]:  # İlk 5 ürünü al
        try:
            name_tag = product.select_one("a[title]")
            name = name_tag["title"] if name_tag else "İsimsiz Ürün"

            price_tag = product.select_one("div.current-price__current")
            price = price_tag.get_text(strip=True) if price_tag else "Fiyat yok"

            link_tag = product.select_one("a[href]")
            link = "https://www.trendyol.com" + link_tag["href"] if link_tag else "#"

            results.append(f"{name}\nFiyat: {price}\n{link}")
        except Exception:
            continue

    return results

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hoş geldiniz! Lütfen aramak istediğiniz ürünü yazın:")

# Mesaj geldiğinde çalışan fonksiyon
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = scrape_trendyol(query)

    if results:
        for result in results:
            await update.message.reply_text(result)
    else:
        await update.message.reply_text("Üzgünüm, ürün bulunamadı. Başka bir ürün deneyin.")

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
