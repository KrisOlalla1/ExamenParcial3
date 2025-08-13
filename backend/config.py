# backend/config.py
import os

class Config:
    # MySQL in XAMPP: user root, no password, host localhost, port 3306
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:@127.0.0.1/medical_appointments")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
