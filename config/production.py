from . import Config

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'  # 운영용 SQLite DB
