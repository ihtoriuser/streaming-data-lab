# Real-Time Data Streaming Pipeline (Kafka → Flink → Superset)

This project implements a real-time data pipeline that simulates a live data stream, processes it in real-time using Apache Flink, and visualizes insights on a Superset dashboard.

## Architecture
`Data Generator` -> `Kafka` -> `Flink` -> `PostgreSQL` -> `Superset`

## Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for local data generator)

## Setup Instructions

### 1. Download Dependencies
Run the PowerShell script to download necessary Flink connector JARs:
```powershell
./download_jars.ps1
```

### 2. Start Infrastructure
Start all services (Kafka, Zookeeper, Flink, PostgreSQL, Superset):
```bash
docker-compose up -d --build
```
*Note: The `--build` flag is important to build the custom Flink image with Python support.*

### 3. Generate Data
Install `kafka-python` if not already installed:
```bash
pip install kafka-python
```
Run the data generator:
```bash
python data_generator.py
```

### 4. Submit Flink Job
Submit the PyFlink job to the Flink cluster:
```bash
docker exec -it streaming-lab-jobmanager-1 ./bin/flink run -py /opt/flink/usrlib/flink_job.py
```
*Note: Adjust container name `streaming-lab-jobmanager-1` if it differs (check with `docker ps`).*

### 5. Verify Data in PostgreSQL
Check if data is being written to the database:
```bash
docker exec -it streaming-lab-postgres-1 psql -U admin -d streaming_db -c "SELECT * FROM device_averages LIMIT 10;"
```

### 6. Configure Superset
1.  Open Superset at `http://localhost:8088` (admin/admin).
2.  Connect to Database:
    -   **Host**: `postgres`
    -   **Port**: `5432`
    -   **Database**: `streaming_db`
    -   **Username**: `admin`
    -   **Password**: `admin`
3.  Create a Dataset from `device_averages`.
4.  Create Charts and Dashboard.

## Components
-   **data_generator.py**: Simulates sensor data.
-   **flink_job.py**: PyFlink job for windowed aggregation.
-   **docker-compose.yml**: Orchestrates the containerized environment.
