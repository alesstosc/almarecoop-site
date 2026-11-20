"""
Modelli SQLAlchemy per la Cooperativa Mitilicoltori Comacchio
Implementazione seguendo le specifiche del paper di riferimento
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """
    Modello per l'autenticazione dell'amministratore
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Imposta la password hashata"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class GlobalSettings(db.Model):
    """
    Modello singleton per le impostazioni globali del sito
    Sempre e solo 1 riga come specificato nel paper
    """
    __tablename__ = 'global_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Identità visiva
    nome_sito = db.Column(db.String(100), nullable=False, default='Cooperativa Mitilicoltori')
    logo_filename = db.Column(db.String(255), nullable=True)
    favicon_filename = db.Column(db.String(255), nullable=True)
    
    # Homepage personalizzabile
    titolo_homepage = db.Column(db.String(200), nullable=False, default='Cooperativa Mitilicoltori Comacchio')
    sottotitolo_homepage = db.Column(db.Text, nullable=False, default='Eccellenza nella produzione di molluschi di alta qualità nelle acque cristalline dell\'Adriatico. Tradizione, sostenibilità e innovazione per portare sulla vostra tavola i migliori prodotti del mare.')
    sfondo_homepage_filename = db.Column(db.String(255), nullable=True)
    
    # Dati legali
    partita_iva = db.Column(db.String(20), nullable=False)
    anno_fondazione = db.Column(db.Integer, nullable=False, default=2024)
    colophon = db.Column(db.Text, nullable=True)  # Ragione sociale, indirizzo, PEC, telefono
    
    # Link social
    facebook_url = db.Column(db.String(255), nullable=True)
    instagram_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    
    # Metadati
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GlobalSettings P.IVA: {self.partita_iva}>'

class ContentCard(db.Model):
    """
    Modello per i contenuti dinamici a "card"
    Cuore del piccolo CMS per gestione contenuti
    """
    __tablename__ = 'content_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(200), nullable=False)
    contenuto = db.Column(db.Text, nullable=False)
    immagine_filename = db.Column(db.String(255), nullable=True)
    sezione = db.Column(db.String(50), nullable=False)  # 'Homepage', 'Prodotti', 'Chi Siamo', etc.
    ordine = db.Column(db.Integer, default=0)  # Per ordinare le card
    
    # Metadati
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<ContentCard {self.titolo} - {self.sezione}>'

class LeadCooperativa(db.Model):
    """
    Modello per i lead del Form 1: Collabora con Noi (Cooperativa)
    Acquisizione contatti da altre cooperative o partner
    """
    __tablename__ = 'lead_cooperativa'
    
    id = db.Column(db.Integer, primary_key=True)
    ragione_sociale = db.Column(db.String(200), nullable=False)
    referente = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    settore = db.Column(db.String(100), nullable=True)
    messaggio = db.Column(db.Text, nullable=True)
    
    # Privacy e metadati
    privacy_accepted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # Per IPv6
    
    def __repr__(self):
        return f'<LeadCooperativa {self.ragione_sociale} - {self.email}>'

class LeadCompratore(db.Model):
    """
    Modello per i lead del Form 2: Area Compratori (Agenti)
    Acquisizione contatti da GDO, ristoratori, grossisti, agenti
    """
    __tablename__ = 'lead_compratore'
    
    id = db.Column(db.Integer, primary_key=True)
    ragione_sociale = db.Column(db.String(200), nullable=False)
    partita_iva = db.Column(db.String(20), nullable=True)
    referente_acquisti = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    tipologia_attivita = db.Column(db.String(100), nullable=False)  # Menu a tendina
    prodotti_interesse = db.Column(db.Text, nullable=True)  # Checkbox serializzate
    messaggio = db.Column(db.Text, nullable=True)
    
    # Privacy e metadati
    privacy_accepted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    
    def __repr__(self):
        return f'<LeadCompratore {self.ragione_sociale} - {self.email}>'

class LeadGenerico(db.Model):
    """
    Modello per i lead del Form 3: Contatti Generali
    Richieste generiche
    """
    __tablename__ = 'lead_generico'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    oggetto = db.Column(db.String(200), nullable=False)
    messaggio = db.Column(db.Text, nullable=False)
    
    # Privacy e metadati
    privacy_accepted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    
    def __repr__(self):
        return f'<LeadGenerico {self.nome_cognome} - {self.email}>'