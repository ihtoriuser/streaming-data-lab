import os

# Получаем URI базы данных из переменной окружения
DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
if DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

# Получаем секретный ключ из переменной окружения
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY")

# Другие возможные настройки
# Например, разрешить загрузку CSV
CSV_EXTENSIONS = {"csv"}
UPLOAD_EXTENSIONS = CSV_EXTENSIONS