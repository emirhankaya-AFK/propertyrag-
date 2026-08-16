# PropertyRAG — Gayrimenkul Analiz ve Yatırım Asistanı

[English](README.md) | [Türkçe](README_TR.md)

PropertyRAG; tapu, ekspertiz ve yapı inceleme belgelerini okuyarak gayrimenkul özelliklerini çıkaran, risk puanları hesaplayan, kredi ve nakit akışı modelleri oluşturan ve alım/geçme raporları hazırlayan bir analiz uygulamasıdır.

## Özellikler

- PDF belge ayrıştırma ve RAG tabanlı sorgulama
- Risk endeksi ve karşılaştırmalı satış analizi
- Kredi amortismanı, nakit akışı, NPV ve IRR hesapları
- FastAPI arka ucu ve Streamlit paneli
- Gemini ve ChromaDB entegrasyonu

## Kurulum

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="api_anahtariniz"
```

API anahtarı yoksa uygulama çevrimdışı geliştirme için örnek yanıt modunda çalışır.

## Çalıştırma

```bash
python -m backend.main
streamlit run frontend/app.py
```

Arka uç `http://127.0.0.1:8002`, OpenAPI belgeleri `/docs` adresinde açılır.

## Testler

```bash
pytest tests/
```

> Bu uygulamadaki mali hesaplamalar bilgilendirme amaçlıdır; yatırım veya kredi tavsiyesi değildir.

