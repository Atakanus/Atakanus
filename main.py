from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import requests
from bs4 import BeautifulSoup

# Telegram Bot Token'ını buraya koy:
BOT_TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"

def trendyol_fiyat_bul(urun_adi):
    url = f"https://www.trendyol.com/sr?q={urun_adi.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    urunler = soup.find_all("div", {"class": "p-card-wrppr"})
    if not urunler:
        return None, None
    fiyat_tag = urunler[0].find("div", {"class": "prc-box-dscntd"})
    if not fiyat_tag:
        fiyat_tag = urunler[0].find("div", {"class": "prc-box-sllng"})
    fiyat = fiyat_tag.text.strip() if fiyat_tag else None
    link_tag = urunler[0].find("a", href=True)
    link = "https://www.trendyol.com" + link_tag['href'] if link_tag else None
    return fiyat, link

def hepsiburada_fiyat_bul(urun_adi):
    url = f"https://www.hepsiburada.com/ara?q={urun_adi.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    urunler = soup.find_all("li", {"class": "search-item"})
    if not urunler:
        return None, None
    fiyat_tag = urunler[0].find("span", {"class": "price-value"})
    fiyat = fiyat_tag.text.strip() if fiyat_tag else None
    link_tag = urunler[0].find("a", href=True)
    link = "https://www.hepsiburada.com" + link_tag['href'] if link_tag else None
    return fiyat, link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ürün adını yaz, en ucuz fiyatı bulayım.\nÖrnek: iPhone 16 Pro Max"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urun = update.message.text.strip()
    trendyol_fiyat, trendyol_link = trendyol_fiyat_bul(urun)
    hepsi_fiyat, hepsi_link = hepsiburada_fiyat_bul(urun)

    if not trendyol_fiyat and not hepsi_fiyat:
        await update.message.reply_text("Üzgünüm, ürün bulunamadı. Başka bir ürün deneyin.")
        return

    mesaj = f"{urun} fiyatları:\n"
    if trendyol_fiyat:
        mesaj += f"- Trendyol: {trendyol_fiyat} TL\nLink: {trendyol_link}\n"
    if hepsi_fiyat:
        mesaj += f"- Hepsiburada: {hepsi_fiyat} TL\nLink: {hepsi_link}\n"

    fiyatlar = {}
    try:
        fiyatlar["Trendyol"] = int(''.join(filter(str.isdigit, trendyol_fiyat)))
    except:
        pass
    try:
        fiyatlar["Hepsiburada"] = int(''.join(filter(str.isdigit, hepsi_fiyat)))
    except:
        pass

    if fiyatlar:
        en_ucuz = min(fiyatlar, key=fiyatlar.get)
        mesaj += f"\n→ En ucuz: {en_ucuz} ({fiyatlar[en_ucuz]} TL)"
    else:
        mesaj += "\n→ En ucuz fiyat bilgisi bulunamadı."

    await update.message.reply_text(mesaj)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
