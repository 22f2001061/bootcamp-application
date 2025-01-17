import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

print(BASE_DIR)


class Config:
    SECRET_KEY = "dev"


class LocalConfig(Config):
    SQLITE_DB_DIR = os.path.join(BASE_DIR, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "project.db")
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "../static/uploads")
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


class ProductionConfig(Config):
    pass
