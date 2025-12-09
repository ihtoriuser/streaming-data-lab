FROM apache/superset:3.1.1

# Устанавливаем правильную версию Werkzeug
COPY requirements-local.txt /app/
RUN pip install --no-cache-dir -r /app/requirements-local.txt

# Копируем наш файл конфигурации
COPY superset_config.py /app/