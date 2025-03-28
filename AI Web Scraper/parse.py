# parse.py - İçerik Ayıklama İşlemleri

import requests
import json
import time
import random
import logging
import re
from dotenv import load_dotenv
import os
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")




sablon = (
    "Aşağıdaki metin içeriğinden belirli bilgileri çıkarmanız isteniyor: {dom_icerik}. "
    "Lütfen bu talimatları dikkatlice izleyin: \n\n"
    "1. Bilgi Çıkarımı: Yalnızca şu açıklamaya uyan bilgileri çıkarın: {ayikla_aciklamasi}. "
    "2. Ekstra İçerik Yok: Cevabınıza başka metin, yorum veya açıklama eklemeyin. "
    "3. Boş Cevap: Eşleşen bilgi yoksa boş string ('') döndürün. "
    "4. Sadece Veri: Çıktınız yalnızca talep edilen veriyi içermeli, başka metin olmamalı."
    "5. Formatlama: Çıktıyı düzenli ve okunabilir bir formatta sunun. Tablolar için düzgün hizalanmış sütunlar kullanın."
)

def format_table_output(text):

    if not text or "|" not in text:
        return text

    lines = text.strip().split('\n')
    if len(lines) < 2:
        return text


    header_line = lines[0]
    headers = [h.strip() for h in header_line.strip('|').split('|')]
    col_widths = [max(len(h), 3) for h in headers]


    for line in lines[2:]:
        if '|' in line:
            cells = [c.strip() for c in line.strip('|').split('|')]
            for i, cell in enumerate(cells):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(cell))


    formatted_lines = []


    header_cells = [h.strip() for h in lines[0].strip('|').split('|')]
    header_line = '| ' + ' | '.join([header_cells[i].ljust(col_widths[i]) for i in range(len(header_cells))]) + ' |'
    formatted_lines.append(header_line)


    separator = '|' + '|'.join(['-' * (col_widths[i] + 2) for i in range(len(col_widths))]) + '|'
    formatted_lines.append(separator)

    for line in lines[2:]:
        if '|' in line:
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == len(col_widths):
                formatted_line = '| ' + ' | '.join([cells[i].ljust(col_widths[i]) for i in range(len(cells))]) + ' |'
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def clean_and_format_json(text):
    try:

        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if json_match:
            json_text = json_match.group(1)
        else:
            json_text = text


        parsed = json.loads(json_text)
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except:

        return text


def icerigi_ayikla(dom_parcalari, ayikla_aciklamasi):
    if not dom_parcalari:
        logger.warning("Ayıklanacak DOM parçası yok!")
        return ""

    logger.info(f"Toplam {len(dom_parcalari)} parça işlenecek.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Web Kaziyici"
    }

    ayiklanan_sonuclar = []

    for i, parca in enumerate(dom_parcalari, start=1):
        try:
            if not parca or not parca.strip():
                logger.info(f"Parça {i} boş, atlanıyor.")
                continue


            if len(parca) > 15000:
                logger.info(f"Parça {i} çok büyük, kısaltılıyor: {len(parca)} -> 15000 karakter")
                parca = parca[:15000]


            format_ipucu = ""
            if "tablo" in ayikla_aciklamasi.lower() or "csv" in ayikla_aciklamasi.lower():
                format_ipucu = "Sonuçları düzgün sıralanmış, sütunları hizalanmış Markdown tablo formatında düzenle."
            elif "json" in ayikla_aciklamasi.lower():
                format_ipucu = "Sonuçları düzgün girintili, geçerli JSON formatında düzenle."


            istek_verisi = {
                "model": "deepseek/deepseek-chat-v3-0324:free",
                "messages": [
                    {
                        "role": "system",
                        "content": sablon.format(
                            dom_icerik=parca,
                            ayikla_aciklamasi=ayikla_aciklamasi
                        ) + (f" {format_ipucu}" if format_ipucu else "")
                    },
                    {
                        "role": "user",
                        "content": "Lütfen sadece talep edilen veriyi düzenli ve okunaklı bir formatta döndürün."
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2048
            }

            logger.info(f"API isteği gönderiliyor: Parça {i}/{len(dom_parcalari)} - {len(parca)} karakter")


            if i > 1:
                wait_time = random.uniform(2, 4)
                logger.info(f"Rate limiting: {wait_time:.1f} saniye bekleniyor...")
                time.sleep(wait_time)

            # İstek gönder
            response = requests.post(
                API_URL,
                headers=headers,
                json=istek_verisi,
                timeout=60
            )


            response.raise_for_status()


            try:
                yanit_json = response.json()
                cevap = yanit_json.get('choices', [{}])[0].get('message', {}).get('content', '')

                if cevap and cevap.strip():

                    if "tablo" in ayikla_aciklamasi.lower() or "csv" in ayikla_aciklamasi.lower() or "|" in cevap:
                        cevap = format_table_output(cevap)
                    elif "json" in ayikla_aciklamasi.lower() or "{" in cevap:
                        cevap = clean_and_format_json(cevap)

                    ayiklanan_sonuclar.append(cevap.strip())
                    logger.info(f"Başarılı: Parça {i}/{len(dom_parcalari)} - '{cevap[:30]}...'")
                else:
                    logger.info(f"Boş cevap: Parça {i}/{len(dom_parcalari)}")
            except Exception as json_error:
                logger.error(f"API yanıt işleme hatası: {str(json_error)}")
                logger.error(f"Ham yanıt: {response.text[:100]}...")

        except requests.exceptions.RequestException as hata:
            logger.error(f"API Hatası (Parça {i}): {str(hata)}")

            time.sleep(5)
        except Exception as hata:
            logger.error(f"Beklenmedik Hata (Parça {i}): {str(hata)}")
            import traceback
            logger.error(traceback.format_exc())


    if "tablo" in ayikla_aciklamasi.lower() or "csv" in ayikla_aciklamasi.lower():

        if len(ayiklanan_sonuclar) > 1:
            merged_result = ayiklanan_sonuclar[0]
            for result in ayiklanan_sonuclar[1:]:
                lines = result.strip().split('\n')
                if len(lines) > 2:
                    data_lines = lines[2:]
                    merged_result += '\n' + '\n'.join(data_lines)
            return format_table_output(merged_result)
        elif len(ayiklanan_sonuclar) == 1:
            return ayiklanan_sonuclar[0]
        else:
            return ""
    elif "json" in ayikla_aciklamasi.lower():
        if len(ayiklanan_sonuclar) > 1:
            try:
                combined_data = []
                for result in ayiklanan_sonuclar:

                    cleaned = clean_and_format_json(result)
                    try:
                        json_data = json.loads(cleaned)
                        if isinstance(json_data, list):
                            combined_data.extend(json_data)
                        else:
                            combined_data.append(json_data)
                    except:
                        logger.warning(f"JSON parse edilemedi: {cleaned[:100]}...")

                return json.dumps(combined_data, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"JSON birleştirme hatası: {str(e)}")

                return "\n\n".join(ayiklanan_sonuclar)
        elif len(ayiklanan_sonuclar) == 1:
            return clean_and_format_json(ayiklanan_sonuclar[0])
        else:
            return ""
    else:

        return "\n\n".join(ayiklanan_sonuclar)