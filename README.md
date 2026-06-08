# Proje 7: IoT ve Akıllı Şehir Uygulaması

## 1. Projenin Amacı ve Kapsamı
Bu projenin amacı, bir akıllı şehir senaryosunda çevreye konumlandırılmış IoT (Nesnelerin İnterneti) cihazlarının/sensörlerinin simüle edilmesi ve bu sensörlerden elde edilen anlık verilerin bulut mimarisi üzerinde güvenli, ölçeklenebilir ve gerçek zamanlı olarak işlenmesini sağlamaktır. 

Proje kapsamında, lokal bir bilgisayar üzerinde çalışacak Python tabanlı simülatör, bir akıllı şehrin sokak lambası, çöp kutusu doluluk oranı ve çevre sıcaklık/nem sensörleri gibi davranacaktır. Üretilen bu anlamlı veriler, MQTT protokolü kullanılarak güvenli bir şekilde AWS IoT Core ortamına aktarılacak, burada tetiklenen AWS Lambda fonksiyonu vasıtasıyla işlenerek depolama katmanına ilesitecektir. Bu çalışma; veri toplama, kuyruğa alma, sunucusuz (serverless) mimari ile veri işleme ve bulut tabanlı izleme süreçlerinin temel mekanizmalarını öğrenmek amacıyla kurgulanmıştır.

## 2. Sistem Mimarisi
Projenin uçtan uca veri akışı ve mimari yapısı aşağıdaki akış şemasına uygun olarak tasarlanmıştır:

```text
+------------------------------------+       MQTT (Secure)       +------------------------+
|                                    | ------------------------> |                        |
|   Lokal Python Script (Sensör)    |                           |   AWS IoT Core (Broker)   |
|  (Sıcaklık, Nem, Doluluk Verisi)   | <------------------------ |                        |
+------------------------------------+                           +------------------------+
                                                                             |
                                                                             | Message Routing / Rule
                                                                             v
+------------------------------------+                           +------------------------+
|                                    |                           |                        |
|   Veritabanı (Depolama Katmanı)    | <------------------------ |  AWS Lambda (Function) |
|      (DynamoDB / PostgreSQL)       |                           |  (Veri Ayrıştırma/Log) |
|                                    |                           |                        |
+------------------------------------+                           +------------------------+