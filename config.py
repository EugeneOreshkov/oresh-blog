import os, json

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    TEMPLATES_AUTO_RELOAD = True

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # Allowed file extensions for uploads (only images)
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp']
    UPLOAD_FOLDER = '/static/customs_avatars'

    # SMTP server address (depends on provider, e.g. smtp.gmail.com, smtp.yandex.ru)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') 
    
    # Port for SMTP: 587 with TLS (recommended) or 465 with SSL
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True'    

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    ADMIN = json.loads(os.environ.get('ADMIN', "[]")) 

    '''
    MAIL_PASSWORD: use an application-specific password,
    not your main email password.

    - For Gmail: Google Account → Security → App passwords
    - For Yandex: Yandex ID → Security → App passwords
    '''

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    POSTS_PER_PAGE = 10