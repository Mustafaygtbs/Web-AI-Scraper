# AI Web Kazıyıcı (Web Scraper)

## Proje Tanımı

AI Web Kazıyıcı, web sitelerinden içerik kazıyan ve yapay zeka teknolojisi ile otomatik olarak veri ayıklama yapabilen gelişmiş bir web scraping aracıdır. Bu uygulama, girilen herhangi bir web sitesinin DOM (Document Object Model) içeriğini çıkarır ve entegre edilmiş yapay zeka API'si ile belirlediğiniz kriterlere göre verileri otomatik olarak ayıklar.

## Özellikler

- Web sitelerinden DOM içeriğini otomatik olarak kazıma
- Yapay zeka ile belirli veri tiplerini (tablo, liste, bilgi vb.) otomatik çıkarma
- Farklı formatlarda veri indirme desteği:
  - Excel (CSV)
  - JSON
  - Metin (TXT)
- Kullanıcı dostu Streamlit arayüzü
- Cloudflare korumalı siteler için gelişmiş konfigürasyon seçenekleri
- HTML dosyasından direkt içerik işleme desteği

## Kullanılan Teknolojiler

- **Python 3** - Ana programlama dili
- **Streamlit** - Web arayüzü için
- **Selenium** - Web sitesi kazıma ve otomasyonu için
- **BeautifulSoup4** - HTML içerik ayıklama ve işleme için
- **Pandas** - Veri işleme ve tablo formatı için
- **OpenPyXL** - Excel formatında dosya oluşturma için
- **Python-dotenv** - Çevre değişkenleri yönetimi
- **OpenRouter AI API** - Akıllı veri ayıklama için yapay zeka servisi

## Kurulum

1. Repoyu klonlayın:
   ```
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

3. `.env` dosyasını oluşturun ve API anahtarlarınızı ekleyin:
   ```
   API_KEY=your_openrouter_api_key_here
   API_URL=https://openrouter.ai/api/v1/chat/completions
   ```

4. Uygulamayı çalıştırın:
   ```
   python -m streamlit run main.py
   ```

## API Anahtarı Edinme

Bu proje, OpenRouter AI servisinin API'sini kullanmaktadır. Ücretsiz bir API anahtarı edinmek için:

1. [OpenRouter.ai](https://openrouter.ai) adresine gidin
2. Bir hesap oluşturun
3. API anahtarınızı oluşturun
4. Bu anahtarı `.env` dosyanıza ekleyin

## Kullanım

1. Web arayüzünde URL girin veya HTML dosyası yükleyin
2. "Web Sitesini Kaz" butonuna tıklayın
3. İçerik kazındıktan sonra, ayıklamak istediğiniz veriyi tanımlayın
4. Çıktı formatını seçin (XLSX, Standart, JSON)
5. "İçeriği Ayıkla" butonuna tıklayın
6. Sonuçları indirin veya kopyalayın

## Örnekler

- **Emlak İlanları**: "Tüm emlak ilanlarını bir tablo olarak listele: başlık, fiyat, oda sayısı, metrekare, konum"
- **Ürün Bilgileri**: "Tüm ürünleri JSON formatında çıkar: isim, fiyat, stok durumu"
- **İletişim Verileri**: "Sayfadaki tüm telefon numaralarını ve e-posta adreslerini listele"

## Not

Bu proje, yalnızca eğitim amaçlı olarak geliştirilmiştir. Web scraping ve verilerin kullanımı konusunda site sahiplerinin kullanım şartlarına ve yasal düzenlemelere uygun hareket edilmelidir. Bu aracı, kullanım şartlarını ihlal edecek şekilde ya da izinsiz veri toplamak için kullanmayınız.

![1](https://github.com/user-attachments/assets/9c7e8286-5ad9-4705-b237-f447fc194ac3)

![2](https://github.com/user-attachments/assets/3727db4b-e476-4c13-9709-bd6606b7fe76)

![3](https://github.com/user-attachments/assets/31ac38a9-3471-467c-ba05-49196f746050)

![4](https://github.com/user-attachments/assets/3137c3e6-941c-452c-a08b-8577de69c83a)

![5](https://github.com/user-attachments/assets/6d047c8e-58af-4964-9338-27d1c4ef8bec)

![6](https://github.com/user-attachments/assets/9f431b62-03f8-4e3e-abf1-e50c8e1909a0)

![7](https://github.com/user-attachments/assets/12e1cbb1-6aab-4f51-9acc-8cea97e8506d)

![8](https://github.com/user-attachments/assets/41ae2fb4-9051-4583-bd92-07c204def90a)


