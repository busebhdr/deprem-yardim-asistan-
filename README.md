# 🧠 Deprem Yardım ve Hazırlık Sistemi (AI Destekli)

Bu proje, afet anlarında sürdürülebilir ve hızlı yardım ulaştırmayı amaçlayan, **Google Gemini AI** ile desteklenmiş bir dijital çözüm platformudur. Hedefimiz, bireylerin afet öncesi bağış yapabilmesini ve afet sonrası ihtiyaçların en hızlı, en verimli şekilde karşılanabilmesini sağlamaktır.

Kullanıcılar sistemde **şehir ve ürün bazlı yardım bağışı kaydı** yapabilir, lojistik firmaları tır sayılarını bildirebilir, ve bir deprem gerçekleştiğinde sistem otomatik olarak:

- 👥 Yardım kayıtlarını analiz eder  
- 📦 Stok durumunu şehir bazında özetler  
- 🚨 Acil durum senaryosu başlatır  
- 🚛 Tır ve market eşleştirmesi yapar  
- 🧠 Yapay zeka ile metinleri anlamsal olarak işler ve öncelik sıralaması yapar

## 🚀 Özellikler

- 📝 Yapılandırılmış Formlar: Ürün ve miktar seçimli bağış formları
- 🧠 Gemini AI Destekli Anlamlandırma: Serbest metinli kayıtlar otomatik olarak analiz edilir
- 📍 Şehir Bazlı Organizasyon: Tüm yardım verileri konuma göre gruplanır
- 🛻 Market & Tır Simülasyonu: Eksik ürünleri en uygun lokasyondan ulaştırma algoritması
- 🚨 Deprem Modu: Simülasyonla tüm sistemi harekete geçiren acil durum aktivasyonu
- 📊 Jüri Paneli: Şehirler arası stok ve yardım durumu özet tablosu
- 🗺️ Harita Tabanlı Görselleştirme (Leaflet.js ile)

## 💡 Yapay Zekanın Rolü

- Serbest metinlerden konum, ürün ve aciliyet bilgisi çıkarma (Gemini AI ile)
- Eksik ürün tahmini ve önceliklendirme
- Doğal dilde yazılmış bağış ve yardım taleplerinin mantıksal düzeltmesi
- En verimli eşleşmeleri öneren analiz modeli

## 🛠️ Kullanılan Teknolojiler

- **Frontend**: HTML, CSS, JavaScript, Leaflet.js
- **Backend**: Python, FastAPI
- **AI/NLP**: Google Gemini API
- **Veritabanı**: MongoDB (motor ile bağlantılı)
- **Konum/Görselleştirme**: OpenStreetMap & Leaflet.js

## 🔧 Kurulum Talimatları

### Gereksinimler

- Python 3.10+
- Google Gemini API anahtarı (Gemini 1.5 modeli)
- MongoDB (local veya Atlas)

### Adımlar

1. Bağımlılıkları yükle:
   ```bash
   pip install fastapi uvicorn motor python-dotenv google-generativeai

2. .env dosyasını oluştur:

GEMINI_API_KEY= buraya kendi API anahtarınızı girin
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=deprem_yardim

3. Sunucuyu başlat:
uvicorn main:app --reload

4. frontend/index.html dosyasını doğrudan tarayıcınızda açın veya bir live server ile görüntüleyin. 

----------------------

🌐 API Endpointleri
POST /analyze → Gemini AI ile metin analizi yapar

POST /submit-entry → Bağış/yardım kayıtlarını sisteme ekler

GET /entries → Tüm kayıtları getirir

POST /simulate-earthquake?konum=X → Acil durum senaryosu başlatır

GET /stock-summary → Şehir bazlı stok özetini getirir

POST /match → Ürün ihtiyaçlarına göre uygun kaynakları eşleştirir

Tüm endpoint'ler için Swagger dokümantasyonu: http://localhost:8000/docs
-----------------------
🧪 Kullanım Senaryosu
Kullanıcı bağış formunu doldurur (ürün + miktar + şehir)

Lojistik firmaları tır sayılarını girer

Deprem gerçekleştiğinde, sistem Simülasyonu Başlat seçeneğiyle aktive edilir

Yapay zeka analizleri yapılır, eksik ürünler belirlenir

En yakın market ve uygun tırlar yönlendirilir

Jüri paneli veya kullanıcı, stok özetlerini ve eşleştirme sonuçlarını görüntüler


✅ Sürdürülebilirlik Katkısı:

Önceden planlanmış kaynak kullanımı

Yerel market işbirlikleri ile hızlı çözüm

Gönüllü katkıların harita bazlı yönlendirilmesi

Gerçek zamanlı veri ile kriz sonrası verimlilik