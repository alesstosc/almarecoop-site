"""
Application Factory per la Cooperativa Mitilicoltori Comacchio
Implementazione seguendo le specifiche del paper di riferimento
"""
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Inizializzazione delle estensioni
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Carica configurazione dal file config.py
    from config import config
    app.config.from_object(config[config_name])
    
    # Assicurati che la directory uploads esista
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inizializzazione estensioni
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configurazione Flask-Login
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Accesso richiesto per visualizzare questa pagina.'
    login_manager.login_message_category = 'info'
    
    # Import dei modelli dopo l'inizializzazione di db
    with app.app_context():
        from app.models import User, GlobalSettings, ContentCard, LeadCooperativa, LeadCompratore, LeadGenerico
    
    # User loader per Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Context processor per rendere GlobalSettings disponibile in tutti i template
    @app.context_processor
    def inject_global_settings():
        settings = GlobalSettings.query.first()
        return dict(global_settings=settings)
    
    # Filtro personalizzato per convertire newline in <br>
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if text is None:
            return ''
        return text.replace('\n', '<br>\n')
    
    # Filtro personalizzato per parsare JSON
    @app.template_filter('from_json')
    def from_json_filter(text):
        if not text:
            return []
        try:
            import json
            return json.loads(text)
        except:
            return []
    
    # Registrazione Blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import request
        # Log solo errori 404 significativi, non quelli di sviluppo frontend
        if not any(path in request.path for path in ['@vite', 'node_modules', '.vite', '/src/']):
            app.logger.warning(f'Pagina non trovata: {request.path} da {request.remote_addr}')
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app