import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer

# Настройки
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'sensor_data'

def generate_data():
    devices = ['sensor-1', 'sensor-2', 'sensor-3']
    
    # Данные
    data = {
        "device_id": random.choice(devices),
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 60.0), 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return data

def main():
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    print(f"Starting data generation to topic '{TOPIC_NAME}'...")
    
    try:
        while True:
            event = generate_data()
            producer.send(TOPIC_NAME, value=event)
            print(f"Sent: {event}")
            time.sleep(1) # Отправляем событие каждую секунду
    except KeyboardInterrupt:
        print("Stopping generator...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()