import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"  # Güvensiz, test için

def scrape_trendyol(query):
    url = f"https://www.trendyol.com/sr?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    items = soup.select("div.p-card-wrppr")[:5]  # İlk 5 ürün

    for item in items:
        try:
            title = item.select_one(".prdct-desc-cntnr-name").get_text(strip=True)
            price_raw = item.select_one(".prc-box-dscntd") or item.select_one(".prc-box-sllng")
            price = price_raw.get_text(strip=True).replace("TL", "").replace(".", "").replace(",", ".")
            link_tag = item.find("a", href=True)
            link = "https://www.trendyol.com" + link_tag["href"] if link_tag else ""

            products.append({
                "title": title,
                "price": float(price),
                "link": link
            })
        except:
            continue  # Hatalı ürün varsa atla

    return sorted(products, key=lambda x: x["price"])

async def ucuzbul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lütfen bir ürün adı girin. Örnek: /ucuzbul airfryer")
        return

    query = "+".join(context.args)
    products = scrape_trendyol(query)

    if not products:
        await update.message.reply_text("Ürün bulunamadı.")
        return

    message = f"En ucuzdan pahalıya ilk 5 ürün:\n\n"
    for p in products:
        message += f"• {p['title']}\nFiyat: {p['price']} TL\n{p['link']}\n\n"

    await update.message.reply_text(message)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ucuzbul", ucuzbul))
    app.run_polling()

if __name__ == "__main__":
    main()
