import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:3620@localhost:3306/vkr?charset=utf8mb4'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
