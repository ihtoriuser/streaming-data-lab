from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(env)

    # Kafka Source Table
    # We use 'kafka:29092' because this script runs inside the Flink container
    # which can access the 'kafka' service on the internal docker network.
    t_env.execute_sql("""
        CREATE TABLE sensor_data (
            device_id STRING,
            temperature DOUBLE,
            humidity DOUBLE,
            `timestamp` STRING,
            ts AS TO_TIMESTAMP(`timestamp`, 'yyyy-MM-dd''T''HH:mm:ss.SSSSSS''Z'''),
            WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'sensor_data',
            'properties.bootstrap.servers' = 'kafka:29092',
            'properties.group.id' = 'flink-group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
    """)

    # PostgreSQL Sink Table
    # We use 'postgres:5432' to access the postgres service.
    t_env.execute_sql("""
        CREATE TABLE device_averages (
            window_end TIMESTAMP(3),
            device_id STRING,
            avg_temp DOUBLE,
            avg_humidity DOUBLE,
            PRIMARY KEY (window_end, device_id) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/streaming_db',
            'table-name' = 'device_averages',
            'username' = 'admin',
            'password' = 'admin'
        )
    """)

    # Aggregation Logic
    # Calculate average temperature and humidity per device every 1 minute
    t_env.execute_sql("""
        INSERT INTO device_averages
        SELECT
            TUMBLE_END(ts, INTERVAL '1' MINUTE) as window_end,
            device_id,
            AVG(temperature) as avg_temp,
            AVG(humidity) as avg_humidity
        FROM sensor_data
        GROUP BY
            device_id,
            TUMBLE(ts, INTERVAL '1' MINUTE)
    """)

if __name__ == '__main__':
    main()
