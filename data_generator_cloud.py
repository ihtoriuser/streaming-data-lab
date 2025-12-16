import time
import json
import random
from datetime import datetime
from confluent_kafka import Producer

# Имя топика
TOPIC_NAME = 'topic_0' # <-- Убедитесь, что это имя вашего топика

def read_config():
    """Читает конфигурацию из файла client.properties"""
    config = {}
    with open("client.properties") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                config[parameter] = value.strip()
    return config

def generate_data():
    """Генерирует одно событие с данными датчика"""
    devices = ['sensor-1', 'sensor-2', 'sensor-3', 'sensor-4', 'sensor-5']
    
    data = {
        "device_id": random.choice(devices),
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "humidity": round(random.uniform(40.0, 65.0), 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return data

def main():
    """Основная функция для запуска генератора"""
    config = read_config()
    
    # Создаем Producer с конфигурацией из файла
    producer = Producer(config)
    
    print(f"Starting data generation to topic '{TOPIC_NAME}'...")
    
    try:
        while True:
            event = generate_data()
            
            # Сериализуем данные в JSON (в виде байтов)
            event_bytes = json.dumps(event).encode('utf-8')
            
            # Отправляем сообщение
            producer.produce(topic=TOPIC_NAME, key=event['device_id'], value=event_bytes)
            print(f"Sent: {event}")
            
            # Важно: producer.poll() нужен для обработки обратных вызовов доставки
            producer.poll(0) 
            
            time.sleep(1) # Отправляем событие каждую секунду
    except KeyboardInterrupt:
        print("Stopping generator...")
    finally:
        # Гарантирует, что все сообщения в буфере будут отправлены
        producer.flush()

if __name__ == "__main__":
    main()