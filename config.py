class Config:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///rental.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False