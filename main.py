import requests
from bs4 import BeautifulSoup

def trendyol_fiyat_bul(urun_adi):
    url = f"https://www.trendyol.com/sr?q={urun_adi.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Ürün kartları genelde 'div' içinde ve class ismi değişmiş olabilir
    urunler = soup.find_all("div", attrs={"class": lambda x: x and "product-card" in x})
    
    if not urunler:
        return None, None

    # İlk ürünü alıyoruz
    ilk_urun = urunler[0]
    
    # Fiyatlar bazen 'div' ya da 'span' içinde olabilir, güncel isimleri kontrol etmek lazım
    fiyat_tag = ilk_urun.find("div", {"class": lambda x: x and ("price" in x or "prc-box" in x)})
    if not fiyat_tag:
        fiyat_tag = ilk_urun.find("span", {"class": lambda x: x and "price" in x})

    fiyat = fiyat_tag.text.strip() if fiyat_tag else None

    link_tag = ilk_urun.find("a", href=True)
    link = "https://www.trendyol.com" + link_tag['href'] if link_tag else None

    return fiyat, link

# Deneme
fiyat, link = trendyol_fiyat_bul("iphone 14")
print(fiyat, link)
