import time
from bs4 import BeautifulSoup
import logging
import traceback


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def website_tara(site_url):

    try:
        logger.info("Undetected Chrome kullanılıyor...")
        import undetected_chromedriver as uc

        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = uc.Chrome(options=options)

        logger.info(f"'{site_url}' adresine bağlanılıyor...")
        driver.get(site_url)


        logger.info("Sayfa yükleniyor (10 saniye bekleniyor)...")
        time.sleep(3)

        html = driver.page_source
        driver.quit()

        logger.info(f"İçerik alındı: {len(html)} karakter")
        return html

    except Exception as e:
        logger.error(f"Undetected Chrome hatası: {str(e)}")
        logger.error(traceback.format_exc())

        try:
            logger.info("Normal Chrome kullanılıyor...")
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')

            options.add_argument(
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

            driver = webdriver.Chrome(options=options)

            logger.info(f"'{site_url}' adresine bağlanılıyor...")
            driver.get(site_url)

            logger.info("Sayfa yükleniyor (10 saniye bekleniyor)...")
            time.sleep(10)

            html = driver.page_source
            driver.quit()

            logger.info(f"İçerik alındı: {len(html)} karakter")
            return html

        except Exception as e:
            logger.error(f"Normal Chrome hatası: {str(e)}")
            logger.error(traceback.format_exc())

            try:
                logger.info("Requests kullanılıyor...")
                import requests

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'tr,en-US;q=0.7,en;q=0.3',
                    'Referer': 'https://www.google.com/',
                    'DNT': '1'
                }

                response = requests.get(site_url, headers=headers, timeout=30)

                if response.status_code == 200:
                    logger.info(f"İçerik alındı: {len(response.text)} karakter")
                    return response.text
                else:
                    logger.error(f"HTTP hata: {response.status_code}")
                    return None

            except Exception as e:
                logger.error(f"Requests hatası: {str(e)}")
                logger.error(traceback.format_exc())
                return None


def govde_icerigini_ayikla(html_content):

    if not html_content:
        logger.warning("HTML içeriği boş!")
        return ""

    try:
        logger.info("HTML içeriği işleniyor...")
        soup = BeautifulSoup(html_content, "html.parser")


        body = soup.body

        if not body:
            logger.warning("Body elementi bulunamadı, tüm HTML kullanılıyor.")
            return html_content

        logger.info("Body içeriği ayıklandı.")
        return str(body)

    except Exception as e:
        logger.error(f"HTML işleme hatası: {str(e)}")
        return html_content


def govde_icerigini_temizle(body_content):

    if not body_content:
        logger.warning("Body içeriği boş!")
        return ""

    try:
        logger.info("Body içeriği temizleniyor...")
        soup = BeautifulSoup(body_content, "html.parser")

        for element in soup(["script", "style", "noscript", "iframe", "svg"]):
            element.decompose()

        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        logger.info(f"Temizlenen içerik boyutu: {len(cleaned_content)} karakter")
        return cleaned_content

    except Exception as e:
        logger.error(f"İçerik temizleme hatası: {str(e)}")
        if isinstance(body_content, str):
            return body_content
        return ""


def dom_icerigini_parcalara_ayir(dom_content, max_length=6000):

    if not dom_content:
        logger.warning("DOM içeriği parçalara ayrılamıyor çünkü boş!")
        return []

    parts = [
        dom_content[i:i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]

    logger.info(f"İçerik {len(parts)} parçaya bölündü.")
    return parts