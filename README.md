Bu proje, OpenAI' dil modelinin API'lerini kullanarak interaktif video senaryolarının otomatik olarak oluşturulmasını sağlar. Kullanıcı dostu bir arayüz sunarak senaryo oluşturma sürecini kolaylaştırır. Proje, farklı senaryo bölümleri (taslak, ana hat, sahneler) için örnekler oluşturarak yaratıcılığı teşvik eder ve kullanıcılara esneklik sağlar.
Nasıl Çalışır
Proje, FastAPI ile oluşturulmuş bir REST API sunar. API, aşağıdaki adımları izleyen bir iş akışı sunar:
Temel Senaryo Oluşturma (/create_main): Kullanıcının girdiği video konusu (GuideFor) temel alınarak OpenAI modeli bir JSON senaryo yapısı oluşturur.
Bölüm Tanımları Ekleme/Güncelleme (/Create_Description): Oluşturulan senaryoya her bölüm için detaylı açıklamalar eklenir veya mevcut örnekler silinir.
Örnekler Oluşturma (/create_draft, /create_outline, /create_scenes): Bu adımlarda senaryonun taslak, ana hat ve sahneler bölümleri için OpenAI modeli kullanılarak örnekler oluşturulur.
Sonuçlandırma (/create_scenes): Son adımda, oluşturulan sahne örnekleri güncellenebilir veya senaryo tamamlanıp dosyaya kaydedilebilir.
Kurulum ve Çalıştırma
Gereksinimler:
Python 3.7+
OpenAI API Anahtarı
FastAPI
Pydantic
Uvicorn (isteğe bağlı, geliştirme sunucusu için)
Gerekli diğer Python paketleri (örneğin, requests, openai)
Kurulum:
Bash
git clone <repository-url>
cd <project-directory>
pip install -r requirements.txt 
.env dosyasında OpenAI API anahtarınızı (OPEN_AI_KEY) ayarlayın.
Çalıştırma (Geliştirme Sunucusu):
Bash
uvicorn app:app --reload
Bu, FastAPI uygulamasını http://127.0.0.1:8080 adresinde başlatacaktır.
Postman Kullanımı
Postman'i indirin ve yükleyin.

Yeni bir istek oluşturun:
HTTP yöntemi: POST
URL: Örneğin, http://127.0.0.1:8080/create_main
Body (Gövde) sekmesi: raw seçeneğini seçin ve JSON formatında ilgili endpointin beklediği veriyi girin. Örneğin, /create_main için:
JSON
{
    "GuideFor": "Eğitim Videosu"
}
Gönder (Send) butonuna tıklayarak isteği gönderin ve API'den yanıtı alın.
Örnek Postman Kodları
POST http://127.0.0.1:8080/create_main
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu"
}
POST http://127.0.0.1:8080/Create_Description
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu",
    "Status": "main_created"  
}
POST http://127.0.0.1:8080/create_draft
Content-Type: application/json

{
    "GuideFor": "Eğitim Videosu",
    "Status": "description_created" 
}
