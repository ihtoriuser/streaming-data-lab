CREATE TABLE device_averages (
    window_end TIMESTAMP,
    device_id VARCHAR(50),
    avg_temp DOUBLE PRECISION,
    avg_humidity DOUBLE PRECISION,
    PRIMARY KEY (window_end, device_id)
);