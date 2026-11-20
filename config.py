"""
File di configurazione per l'applicazione Flask
Seguendo le specifiche del paper di riferimento
"""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurazione base"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY non impostata. Copia .env.example in .env e valorizzala, "
            "oppure esportala nell'ambiente prima di avviare l'applicazione."
        )
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurazione upload file
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico', 'svg'}
    
    # Configurazione Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Configurazione email (per invio notifiche form)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'

class DevelopmentConfig(Config):
    """Configurazione per sviluppo (DEBUG solo se richiesto esplicitamente)"""
    DEBUG = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')

class ProductionConfig(Config):
    """Configurazione per produzione"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}