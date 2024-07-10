
**Amaç**

Bu proje, OpenAI dil modelinin API'lerini kullanarak interaktif video senaryolarının otomatik olarak oluşturulmasını sağlar. Kullanıcı dostu bir arayüz sunarak senaryo oluşturma sürecini kolaylaştırır. Proje, farklı senaryo bölümleri (taslak, ana hat, sahneler) için örnekler oluşturarak yaratıcılığı teşvik eder ve kullanıcılara esneklik sağlar.

**Nasıl Çalışır**

Proje, FastAPI ile oluşturulmuş bir REST API sunar. API, aşağıdaki adımları izleyen bir iş akışı sunar:

1. **Temel Senaryo Oluşturma (`/create_main`)**: Kullanıcının girdiği video konusu (GuideFor) temel alınarak OpenAI modeli bir JSON senaryo yapısı oluşturur.
2. **Bölüm Tanımları Ekleme/Güncelleme (`/Create_Description`)**: Oluşturulan senaryoya her bölüm için detaylı açıklamalar eklenir veya mevcut örnekler silinir.
3. **Örnekler Oluşturma (`/create_draft`, `/create_outline`, `/create_scenes`)**: Bu adımlarda senaryonun taslak, ana hat ve sahneler bölümleri için OpenAI modeli kullanılarak örnekler oluşturulur.
4. **Sonuçlandırma (`/create_scenes`)**: Son adımda, oluşturulan sahne örnekleri güncellenebilir veya senaryo tamamlanıp dosyaya kaydedilebilir.


2. **Kurulum:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   pip install -r requirements.txt 
   ```
   `.env` dosyasında OpenAI API anahtarınızı (`OPEN_AI_KEY`) ayarlayın.

3. **Çalıştırma (Geliştirme Sunucusu):**
   ```bash
   uvicorn app:app --reload
   ```
   Bu, FastAPI uygulamasını http://127.0.0.1:8080 adresinde başlatacaktır.

**Postman Kullanımı**

1. **Postman'i indirin ve yükleyin.**
2. **Yeni bir istek oluşturun:**
    - HTTP yöntemi: `POST`
    - URL: Örneğin, `http://127.0.0.1:8080/create_main`
    - Body (Gövde) sekmesi: `raw` seçeneğini seçin ve JSON formatında ilgili endpointin beklediği veriyi girin. Örneğin, `/create_main` için:

    ```json
    {
        "GuideFor": "Eğitim Videosu"
    }
    ```
3. **Gönder (Send)** butonuna tıklayarak isteği gönderin ve API'den yanıtı alın.

**Örnek Postman Kodları**

```
POST http://127.0.0.1:8080/create_main
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu"
}
```
```
POST http://127.0.0.1:8080/Create_Description
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu",
    "Status": "main_created"  
}
```

```
POST http://127.0.0.1:8080/create_draft
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu",
    "Status": "description_created" 
}
```

