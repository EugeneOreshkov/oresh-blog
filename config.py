import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    TEMPLATES_AUTO_RELOAD = True

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'webp')
    # UPLOADED_PHOTOS_ROOT