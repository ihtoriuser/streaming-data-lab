from pyflink.table import EnvironmentSettings, TableEnvironment

def main():
    # 1. Настройка окружения
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)

    # 2. Создание источника (Kafka)
    # Мы описываем, как читать JSON из Kafka
    t_env.execute_sql("""
        CREATE TABLE sensor_source (
            device_id STRING,
            temperature DOUBLE,
            humidity DOUBLE,
            `timestamp` TIMESTAMP(3),
            WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'sensor_data',
            'properties.bootstrap.servers' = 'kafka:29092',
            'properties.group.id' = 'flink-group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
    """)

    # 3. Создание стока (Postgres)
    # Мы описываем, куда писать результат
    t_env.execute_sql("""
        CREATE TABLE postgres_sink (
            window_end TIMESTAMP(3),
            device_id STRING,
            avg_temp DOUBLE,
            PRIMARY KEY (window_end, device_id) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/streaming_db',
            'table-name' = 'device_averages',
            'username' = 'admin',
            'password' = 'admin'
        )
    """)

    # 4. Логика обработки (SQL Query)
    # Группируем по "Tumbling Window" (1 минута) и считаем среднее
    t_env.execute_sql("""
        INSERT INTO postgres_sink
        SELECT
            TUMBLE_END(`timestamp`, INTERVAL '1' MINUTE) as window_end,
            device_id,
            AVG(temperature) as avg_temp
        FROM sensor_source
        GROUP BY
            device_id,
            TUMBLE(`timestamp`, INTERVAL '1' MINUTE)
    """)

if __name__ == '__main__':
    main()