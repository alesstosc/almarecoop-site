"""
Form WTForms per l'area amministrativa
Cooperativa Mitilicoltori Comacchio
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    """Form di login per l'amministratore"""
    username = StringField(
        'Username',
        validators=[DataRequired(message='Campo obbligatorio')],
        render_kw={'class': 'form-control', 'placeholder': 'Username'}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Campo obbligatorio')],
        render_kw={'class': 'form-control', 'placeholder': 'Password'}
    )
    
    remember_me = BooleanField(
        'Ricordami',
        render_kw={'class': 'form-check-input'}
    )

class GlobalSettingsForm(FlaskForm):
    """
    Form per la gestione delle impostazioni globali (GlobalSettings)
    Modifica dell'unica riga della tabella come specificato nel paper
    """
    # Identità visiva
    nome_sito = StringField(
        'Nome del Sito *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Nome della cooperativa'}
    )
    
    logo = FileField(
        'Logo',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'svg'], 'Solo immagini consentite!')
        ],
        render_kw={'class': 'form-control'}
    )
    
    favicon = FileField(
        'Favicon',
        validators=[
            FileAllowed(['ico', 'png', 'gif'], 'Solo file .ico, .png, .gif consentiti!')
        ],
        render_kw={'class': 'form-control'}
    )
    
    # Homepage personalizzabile
    titolo_homepage = StringField(
        'Titolo Homepage *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Titolo principale della homepage'}
    )
    
    sottotitolo_homepage = TextAreaField(
        'Sottotitolo Homepage *',
        validators=[DataRequired(message='Campo obbligatorio')],
        render_kw={
            'class': 'form-control', 
            'rows': 4,
            'placeholder': 'Descrizione che apparirà sotto il titolo principale...'
        }
    )
    
    sfondo_homepage = FileField(
        'Sfondo Homepage',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo immagini consentite!')
        ],
        render_kw={'class': 'form-control'}
    )
    
    # Dati legali
    partita_iva = StringField(
        'Partita IVA *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=20)],
        render_kw={'class': 'form-control', 'placeholder': 'IT12345678901'}
    )
    
    anno_fondazione = IntegerField(
        'Anno di Fondazione *',
        validators=[DataRequired(message='Campo obbligatorio'), NumberRange(min=1900, max=2100)],
        render_kw={'class': 'form-control', 'placeholder': '2024'}
    )
    
    colophon = TextAreaField(
        'Colophon (Dati Cooperativa)',
        validators=[Optional()],
        render_kw={
            'class': 'form-control', 
            'rows': 8,
            'placeholder': 'Ragione Sociale\nIndirizzo sede legale/operativa\nPEC\nTelefono\n...'
        }
    )
    
    # Link social
    facebook_url = StringField(
        'URL Facebook',
        validators=[Optional(), Length(max=255)],
        render_kw={'class': 'form-control', 'placeholder': 'https://facebook.com/cooperativa'}
    )
    
    instagram_url = StringField(
        'URL Instagram',
        validators=[Optional(), Length(max=255)],
        render_kw={'class': 'form-control', 'placeholder': 'https://instagram.com/cooperativa'}
    )
    
    linkedin_url = StringField(
        'URL LinkedIn',
        validators=[Optional(), Length(max=255)],
        render_kw={'class': 'form-control', 'placeholder': 'https://linkedin.com/company/cooperativa'}
    )

class ContentCardForm(FlaskForm):
    """
    Form per la gestione delle ContentCard
    Cuore del piccolo CMS per contenuti dinamici
    """
    titolo = StringField(
        'Titolo *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Titolo della card'}
    )
    
    contenuto = TextAreaField(
        'Contenuto *',
        validators=[DataRequired(message='Campo obbligatorio')],
        render_kw={
            'class': 'form-control', 
            'rows': 6,
            'placeholder': 'Contenuto della card (supporta HTML base)'
        }
    )
    
    immagine = FileField(
        'Immagine (opzionale)',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'svg'], 'Solo immagini consentite!')
        ],
        render_kw={'class': 'form-control'}
    )
    
    sezione = SelectField(
        'Sezione *',
        validators=[DataRequired(message='Campo obbligatorio')],
        choices=[
            ('Homepage', 'Homepage'),
            ('Chi Siamo', 'Chi Siamo'),
            ('Prodotti', 'Prodotti'),
            ('News', 'News')
        ],
        render_kw={'class': 'form-select'}
    )
    
    ordine = IntegerField(
        'Ordine',
        validators=[Optional(), NumberRange(min=0, max=999)],
        default=0,
        render_kw={'class': 'form-control', 'placeholder': '0'}
    )
    
    is_active = BooleanField(
        'Attiva',
        default=True,
        render_kw={'class': 'form-check-input'}
    )