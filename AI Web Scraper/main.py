# main.py - Ana Uygulama Dosyası
# Programı çalıştırmak için konsola: python -m streamlit run main.py

import streamlit as st
from scrape import (
    website_tara,
    govde_icerigini_ayikla,
    govde_icerigini_temizle,
    dom_icerigini_parcalara_ayir,
)
from parse import icerigi_ayikla
import traceback
import re
import os
import logging
import json
import pandas as pd
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="AI Web Kazıyıcı",
    page_icon="🔍",
    layout="wide"
)


st.markdown("""
<style>
    /* Ana renkler ve stiller */
    :root {
        --primary-color: #2563EB;
        --primary-light: #DBEAFE;
        --primary-dark: #1E40AF;
        --text-color: #1F2937;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --error-color: #EF4444;
        --card-bg: #FFFFFF;
    }

    .main {
        background-color: #F9FAFB;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
    }

    /* Metin kutusu stillerinin düzeltilmesi */
    .stTextArea>div>div>textarea {
        color: var(--text-color) !important;
        background-color: white !important;
        border: 1px solid #D1D5DB;
        font-family: monospace;
    }

    /* Text input stillerinin düzeltilmesi */
    .stTextInput>div>div>input {
        color: var(--text-color) !important;
        background-color: white !important;
        border: 1px solid #D1D5DB;
    }

    /* Kod blokları stillerinin düzeltilmesi */
    pre {
        background-color: #F3F4F6 !important;
        padding: 10px;
        border-radius: 5px;
        color: #1F2937 !important;
        border: 1px solid #E5E7EB;
    }

    code {
        color: #1F2937 !important;
    }

    /* Buton stillendirilmesi */
    .stButton>button {
        background-color: var(--primary-color);
        color: white !important;
        font-weight: 500;
        border-radius: 0.375rem;
        border: none;
    }

    /* Data frame stillendirilmesi */
    .dataframe {
        width: 100%;
        font-size: 0.9rem;
    }

    .dataframe th {
        background-color: #F3F4F6;
        color: var(--text-color);
        font-weight: 600;
        text-align: left;
        padding: 12px;
        border-bottom: 2px solid #D1D5DB;
    }

    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #E5E7EB;
        color: var(--text-color);
    }

    /* Bildirim kutuları */
    .info-box {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }

    .warning-box {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }

    .success-box {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }

    .error-box {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }

    /* Tablo stillendirilmesi için */
    .table-results {
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* İndirme butonları için */
    .download-btn {
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


st.title("🔍 AI Web Kazıyıcı")
st.markdown("Web sitelerinden veri toplamak ve içerik ayıklamak için geliştirilmiştir")


tab1, tab2 = st.tabs(["💻 Web Sitesi Kazıma", "📁 Dosyadan Yükleme"])

with tab1:

    col1, col2 = st.columns([4, 1])
    with col1:
        url = st.text_input("Website URL'sini Girin", placeholder="https://example.com")
    with col2:

        kaz_button = st.button("Web Sitesini Kaz", use_container_width=True)

    if kaz_button:
        if url:
            with st.spinner("Web sitesi kazınıyor..."):
                try:
                    progress_text = st.empty()
                    progress_text.info("Sayfa içeriği alınıyor. Bu işlem birkaç saniye sürebilir...")


                    ham_dom = website_tara(url)

                    if ham_dom and ("Cloudflare" in ham_dom and "challenge" in ham_dom):
                        st.error(
                            "⚠️ Cloudflare tarafından engellendiniz! Undetected Chrome deneyin veya Dosyadan Yükleme sekmesini kullanın.")
                        st.stop()

                    if ham_dom and len(ham_dom) > 500:

                        st.session_state.content_size = len(ham_dom)


                        govde_icerik = govde_icerigini_ayikla(ham_dom)

                        if govde_icerik:

                            temizlenmis_icerik = govde_icerigini_temizle(govde_icerik)

                            if temizlenmis_icerik and len(temizlenmis_icerik) > 100:

                                st.session_state.dom_icerik = temizlenmis_icerik
                                st.session_state.ham_dom = ham_dom


                                st.success(
                                    f"Web sitesi başarıyla kazındı! İçerik boyutu: {len(temizlenmis_icerik)} karakter")


                                with st.expander("DOM İçeriğini Görüntüle"):
                                    st.text_area("İçerik Önizleme", temizlenmis_icerik[:5000] + (
                                        "..." if len(temizlenmis_icerik) > 5000 else ""), height=200)
                            else:
                                st.error("İçerik temizlendikten sonra çok az metin kaldı.")
                        else:
                            st.error("HTML içeriğinden içerik ayıklanamadı.")
                    else:
                        st.error(f"Web sitesi içeriği alınamadı veya çok kısa.")

                except Exception as e:
                    st.error(f"Hata oluştu: {str(e)}")
                    with st.expander("Hata Detayları"):
                        st.code(traceback.format_exc())
        else:
            st.warning("Lütfen bir URL girin.")

with tab2:
    st.subheader("📁 HTML Dosyasından Yükleme")

    st.info("""
    Web sitesini doğrudan kazıyamıyorsanız, HTML dosyasını yükleyebilirsiniz:
    1. Web sitesini normal tarayıcınızla açın
    2. "Kaynağı Görüntüle" seçeneğiyle tüm HTML'i kopyalayın
    3. Bir metin dosyasına yapıştırıp .html uzantısıyla kaydedin
    """)

    uploaded_file = st.file_uploader("HTML Dosyası Yükle", type=["html", "htm", "txt"])

    if uploaded_file:

        content = uploaded_file.read().decode("utf-8", errors="replace")

        if content:
            try:

                st.session_state.ham_dom = content
                st.session_state.content_size = len(content)


                govde_icerik = govde_icerigini_ayikla(content)

                if govde_icerik:

                    temizlenmis_icerik = govde_icerigini_temizle(govde_icerik)

                    if temizlenmis_icerik and len(temizlenmis_icerik) > 100:

                        st.session_state.dom_icerik = temizlenmis_icerik


                        st.success(f"Dosya başarıyla işlendi: {uploaded_file.name}")


                        with st.expander("DOM İçeriğini Görüntüle"):
                            st.text_area("İçerik Önizleme",
                                         temizlenmis_icerik[:5000] + ("..." if len(temizlenmis_icerik) > 5000 else ""),
                                         height=200)
                    else:
                        st.error("İçerik temizlendikten sonra çok az metin kaldı.")
                else:
                    st.error("HTML içeriğinden body ayıklanamadı.")

            except Exception as e:
                st.error(f"Dosya işleme hatası: {str(e)}")
                with st.expander("Hata Detayları"):
                    st.code(traceback.format_exc())


    try:
        if os.path.exists("fallback_example.html"):
            if st.button("Örnek HTML'i Kullan"):
                with open("fallback_example.html", "r", encoding="utf-8") as f:
                    example_html = f.read()


                st.session_state.ham_dom = example_html
                st.session_state.content_size = len(example_html)

                govde_icerik = govde_icerigini_ayikla(example_html)
                temizlenmis_icerik = govde_icerigini_temizle(govde_icerik)
                st.session_state.dom_icerik = temizlenmis_icerik

                st.success("Örnek HTML başarıyla yüklendi!")
    except:
        pass


if "dom_icerik" in st.session_state:
    st.markdown("---")
    st.subheader("🔍 İçerik Ayıklama")


    col1, col2 = st.columns([3, 1])

    with col1:
        ayikla_aciklamasi = st.text_input(
            "Ayıklamak istediğiniz veriyi tanımlayın",
            placeholder="Örnek: Tüm emlak ilanlarını bir tablo olarak listele: başlık, fiyat, oda sayısı, metrekare, konum"
        )

    with col2:
        cikti_format = st.selectbox(
            "Çıktı Formatı",
            ["Tablo (CSV)", "Standart", "JSON"],
            index=0
        )

    if st.button("İçeriği Ayıkla", use_container_width=True):
        if ayikla_aciklamasi:
            with st.spinner("AI modeliyle içerik ayıklanıyor..."):
                try:

                    format_istegi = ""
                    if cikti_format == "Tablo (CSV)":
                        format_istegi = """
                        Sonuçları tablo formatında düzenle. Başlıkları ve sütunları tam hizalı olacak şekilde ayarla. 
                        Tablo formatı için şunlara dikkat et:
                        1. Başlık satırı, ayırıcı çizgi ve veri satırları olmalı
                        2. Sütunlar '|' karakteriyle ayrılmalı
                        3. Hücre içeriğindeki bilgiler temiz ve düzenli olmalı
                        4. Boş değerler için '-' kullan
                        5. Sütun başlıkları kısa ve anlaşılır olmalı
                        """
                    elif cikti_format == "JSON":
                        format_istegi = "Sonuçları düzgün girintili, geçerli JSON formatında döndür."


                    if format_istegi:
                        tam_aciklama = f"{ayikla_aciklamasi}. {format_istegi}"
                    else:
                        tam_aciklama = ayikla_aciklamasi


                    dom_parcalari = dom_icerigini_parcalara_ayir(st.session_state.dom_icerik, 4000)


                    ayiklanan_sonuc = icerigi_ayikla(dom_parcalari, tam_aciklama)

                    if ayiklanan_sonuc:

                        if cikti_format == "Tablo (CSV)" and "|" in ayiklanan_sonuc:
                            try:

                                lines = [line.strip() for line in ayiklanan_sonuc.strip().split('\n')]
                                if len(lines) >= 2:

                                    headers = [h.strip() for h in lines[0].strip('|').split('|')]


                                    data = []
                                    for line in lines[2:]:
                                        if line.strip() and '|' in line:
                                            row = [cell.strip() for cell in line.strip('|').split('|')]
                                            if len(row) == len(headers):
                                                data.append(row)


                                    df = pd.DataFrame(data, columns=headers)

                                    st.header("Ayıklanan Veriler")
                                    st.dataframe(df, use_container_width=True)

                                    csv = df.to_csv(index=False)
                                    file_name = f"ayiklanan_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.download_button(
                                            label="CSV Olarak İndir",
                                            data=csv,
                                            file_name=file_name,
                                            mime="text/csv",
                                        )
                                    with col2:
                                        st.download_button(
                                            label="Metin Olarak İndir",
                                            data=ayiklanan_sonuc,
                                            file_name=file_name.replace(".csv", ".txt"),
                                            mime="text/plain",
                                        )

                                    with st.expander("Ham Tablo Sonucu"):
                                        st.code(ayiklanan_sonuc)
                                else:

                                    st.header("Ayıklanan Sonuç")
                                    st.text_area("", ayiklanan_sonuc, height=300)

                                    file_name = f"ayiklanan_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                    st.download_button(
                                        label="Metin Olarak İndir",
                                        data=ayiklanan_sonuc,
                                        file_name=file_name,
                                        mime="text/plain",
                                    )
                            except Exception as e:

                                st.warning(f"Tablo dönüşümünde hata: {str(e)}")
                                st.header("Ayıklanan Sonuç")
                                st.text_area("", ayiklanan_sonuc, height=300)

                        elif cikti_format == "JSON":
                            try:

                                json_match = re.search(r'```json\s*([\s\S]*?)\s*```', ayiklanan_sonuc)
                                if json_match:
                                    json_text = json_match.group(1)
                                    json_data = json.loads(json_text)
                                else:
                                    json_data = json.loads(ayiklanan_sonuc)

                                pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)

                                st.header("Ayıklanan JSON")
                                st.json(json_data)

                                # JSON dosyası olarak indirme
                                file_name = f"ayiklanan_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.download_button(
                                        label="JSON Olarak İndir",
                                        data=pretty_json,
                                        file_name=file_name,
                                        mime="application/json",
                                    )
                                with col2:
                                    st.download_button(
                                        label="Metin Olarak İndir",
                                        data=ayiklanan_sonuc,
                                        file_name=file_name.replace(".json", ".txt"),
                                        mime="text/plain",
                                    )
                            except json.JSONDecodeError:
                                # JSON formatı değilse ham metni göster
                                st.warning("Sonuç geçerli bir JSON formatında değil.")
                                st.header("Ayıklanan Sonuç")
                                st.text_area("", ayiklanan_sonuc, height=300)

                                # Metin olarak indirme butonu
                                file_name = f"ayiklanan_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                                st.download_button(
                                    label="Metin Olarak İndir",
                                    data=ayiklanan_sonuc,
                                    file_name=file_name,
                                    mime="text/plain",
                                )

                        else:  # Standart format
                            st.header("Ayıklanan Sonuç")
                            st.text_area("", ayiklanan_sonuc, height=300)

                            file_name = f"ayiklanan_veri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            st.download_button(
                                label="Metin Olarak İndir",
                                data=ayiklanan_sonuc,
                                file_name=file_name,
                                mime="text/plain",
                            )

                        st.success("İçerik başarıyla ayıklandı!")
                    else:
                        st.warning("Belirtilen veriye uygun içerik bulunamadı.")

                except Exception as e:
                    st.error(f"İçerik ayıklama sırasında hata oluştu: {str(e)}")
                    with st.expander("Hata Detayları"):
                        st.code(traceback.format_exc())
        else:
            st.warning("Lütfen ayıklamak istediğiniz veriyi tanımlayın.")


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4B5563; font-size: 0.8rem;">
    <p>AI Web Kazıyıcı &copy; 2025 | Bu uygulama, eğitim amaçlıdır. Mustafa YİĞİTBAŞI tarafından geliştirilmiştir.</p>
</div>
""", unsafe_allow_html=True)