import time
import json
import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# --- AYARLAR ---
ENDPOINT = "a3lbtii9bbycol-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "Akilli_Sehir_Sensoru"
TOPIC = "akillisehir/sensor1"

# --- SERTİFİKA YOLLARI 
CA_PATH = "certs/AmazonRootCA1.pem"       
CERT_PATH = "certs/device.pem.crt.crt"   
KEY_PATH = "certs/private.pem.key.key"   

# --- AWS BAĞLANTI AYARLARI ---
myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

# Bağlantı Sorunlarını Önlemek İçin Zaman Aşımı Ayarları
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

# --- BULUTA BAĞLAN ---
print("AWS IoT Core'a güvenli bağlantı kuruluyor...")
myMQTTClient.connect()
print("Bağlantı BAŞARILI! Canlı veri akışı başlıyor...\n")

# --- CANLI VERİ SİMÜLASYONU ---
try:
    while True:
        # Sahte Akıllı Şehir Verileri Üretme
        sicaklik = round(random.uniform(15.0, 35.0), 2)
        nem = round(random.uniform(40.0, 80.0), 2)
        cop_kutusu_doluluk = random.randint(0, 100) # % cinsinden
        
        payload = {
            "cihaz_id": CLIENT_ID,
            "timestamp": int(time.time()),
            "sicaklik": sicaklik,
            "nem": nem,
            "cop_doluluk_orani": cop_kutusu_doluluk
        }
        
        # JSON formatına çevirip buluta fırlatıyoruz
        myMQTTClient.publish(TOPIC, json.dumps(payload), 1)
        print(f"Buluta Gönderilen Veri: {payload}")
        
        # 5 saniyede bir veri gönder
        time.sleep(5)

except KeyboardInterrupt:
    print("\nVeri akışı kullanıcı tarafından durduruldu.")
    myMQTTClient.disconnect()