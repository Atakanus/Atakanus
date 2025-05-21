from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import requests
from bs4 import BeautifulSoup

TOKEN = "7922168827:AAFxAJurX5SLlZI1pua_FHQWgqrLSe9DHk4"  # Tokeni buraya koyduk

def trendyol_fiyat_bul(urun_adi):
    url = f"https://www.trendyol.com/sr?q={urun_adi.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=7)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        urunler = soup.find_all("div", {"class": "p-card-wrppr"})
        if not urunler:
            return None, None
        # İlk ürün fiyat ve link
        fiyat_tag = urunler[0].find("div", {"class": "prc-box-dscntd"})
        if not fiyat_tag:
            fiyat_tag = urunler[0].find("div", {"class": "prc-box-sllng"})
        fiyat = fiyat_tag.text.strip() if fiyat_tag else None
        link_tag = urunler[0].find("a", href=True)
        link = "https://www.trendyol.com" + link_tag['href'] if link_tag else None
        return fiyat, link
    except Exception:
        return None, None

def hepsiburada_fiyat_bul(urun_adi):
    url = f"https://www.hepsiburada.com/ara?q={urun_adi.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=7)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        urunler = soup.find_all("li", {"class": "search-item"})
        if not urunler:
            return None, None
        fiyat_tag = urunler[0].find("span", {"class": "price-value"})
        fiyat = fiyat_tag.text.strip() if fiyat_tag else None
        link_tag = urunler[0].find("a", href=True)
        link = "https://www.hepsiburada.com" + link_tag['href'] if link_tag else None
        return fiyat, link
    except Exception:
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ürün adını yaz, Trendyol ve Hepsiburada'dan en ucuz fiyatı bulayım.\n"
        "Örnek: iPhone 13 Pro Max"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urun = update.message.text.strip()
    trendyol_fiyat, trendyol_link = trendyol_fiyat_bul(urun)
    hepsi_fiyat, hepsi_link = hepsiburada_fiyat_bul(urun)

    if not trendyol_fiyat and not hepsi_fiyat:
        await update.message.reply_text("Üzgünüm, ürün bulunamadı. Başka bir ürün deneyin.")
        return

    mesaj = f"📦 {urun} fiyatları:\n"
    fiyatlar = {}

    if trendyol_fiyat and trendyol_link:
        mesaj += f"- Trendyol: {trendyol_fiyat} TL\n  [Ürünü Görmek İçin Tıkla]({trendyol_link})\n"
        try:
            fiyatlar["Trendyol"] = int(''.join(filter(str.isdigit, trendyol_fiyat)))
        except: 
            pass

    if hepsi_fiyat and hepsi_link:
        mesaj += f"- Hepsiburada: {hepsi_fiyat} TL\n  [Ürünü Görmek İçin Tıkla]({hepsi_link})\n"
        try:
            fiyatlar["Hepsiburada"] = int(''.join(filter(str.isdigit, hepsi_fiyat)))
        except: 
            pass

    if fiyatlar:
        en_ucuz = min(fiyatlar, key=fiyatlar.get)
        mesaj += f"\n💰 En ucuz fiyat: {en_ucuz} ({fiyatlar[en_ucuz]} TL)"
    else:
        mesaj += "\n⚠️ En ucuz fiyat bilgisi alınamadı."

    await update.message.reply_text(mesaj, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot başladı...")
    app.run_polling()

if __name__ == "__main__":
    main()
