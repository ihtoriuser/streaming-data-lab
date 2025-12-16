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
        bootstrap_servers="pkc-75m1o.europe-west3.gcp.confluent.cloud:9092", # Ваш Bootstrap Server
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_plain_username="MFSVMC2KBO6GQ7O6", # Ваш Kafka API Key
        sasl_plain_password="cflt8V96z7MZQfhErX49FycBsVXpd14rnxgW+N/6JJ2psC4p9JX10envuif20mBw", # Ваш Kafka API Secret
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
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