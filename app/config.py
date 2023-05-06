import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Redis settings
    REDIS_HOST = os.environ.get('REDIS_HOST') or '3000'
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))

    # MongoDB settings
    MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')