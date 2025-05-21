from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import requests
from bs4 import BeautifulSoup

# Telegram Bot Token (senin botunun token'ı)
TOKEN = "7060381492:AAG0eZejT6YNe3SGPQkqHTULCZeh0BjjPbM"

# Trendyol Scraper
def trendyol_fiyat_bul(urun_adi):
    url = f"https://www.trendyol.com/sr?q={urun_adi.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    urunler = soup.find_all("li", class_="product-item")
    if not urunler:
        return None, None

    for urun in urunler:
        fiyat_tag = urun.find("div", class_="current-price__current")
        link_tag = urun.find("a", href=True)

        if fiyat_tag and link_tag:
            fiyat = fiyat_tag.text.strip().replace("\n", "").replace("TL", "").strip()
            link = "https://www.trendyol.com" + link_tag['href']
            return fiyat, link

    return None, None

# Hepsiburada Scraper
def hepsiburada_fiyat_bul(urun_adi):
    url = f"https://www.hepsiburada.com/ara?q={urun_adi.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    urunler = soup.find_all("li", {"class": "search-item"})
    if not urunler:
        return None, None

    for urun in urunler:
        fiyat_tag = urun.find("span", class_="price-value")
        link_tag = urun.find("a", href=True)

        if fiyat_tag and link_tag:
            fiyat = fiyat_tag.text.strip().replace("TL", "").strip()
            link = "https://www.hepsiburada.com" + link_tag["href"]
            return fiyat, link

    return None, None

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ürün adını yaz, Trendyol ve Hepsiburada'daki en ucuz fiyatı bulayım.\nÖrnek: iPhone 16 Pro Max"
    )

# Kullanıcı mesajlarını işleyelim
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urun = update.message.text.strip()

    trendyol_fiyat, trendyol_link = trendyol_fiyat_bul(urun)
    hepsi_fiyat, hepsi_link = hepsiburada_fiyat_bul(urun)

    if not trendyol_fiyat and not hepsi_fiyat:
        await update.message.reply_text("Üzgünüm, ürün bulunamadı. Başka bir ürün deneyin.")
        return

    mesaj = f"'{urun}' için fiyatlar:\n"
    fiyatlar = {}

    if trendyol_fiyat:
        mesaj += f"- Trendyol: {trendyol_fiyat} TL\n{trendyol_link}\n"
        try:
            fiyatlar["Trendyol"] = int(''.join(filter(str.isdigit, trendyol_fiyat)))
        except:
            pass

    if hepsi_fiyat:
        mesaj += f"- Hepsiburada: {hepsi_fiyat} TL\n{hepsi_link}\n"
        try:
            fiyatlar["Hepsiburada"] = int(''.join(filter(str.isdigit, hepsi_fiyat)))
        except:
            pass

    if fiyatlar:
        en_ucuz = min(fiyatlar, key=fiyatlar.get)
        mesaj += f"\n→ En ucuz: {en_ucuz} ({fiyatlar[en_ucuz]} TL)"
    else:
        mesaj += "\n→ En ucuz fiyat belirlenemedi."

    await update.message.reply_text(mesaj)

# Botu başlat
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
