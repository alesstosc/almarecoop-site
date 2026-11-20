"""
Form WTForms per l'acquisizione lead
Cooperativa Mitilicoltori Comacchio
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import CheckboxInput, ListWidget

class MultiCheckboxField(SelectMultipleField):
    """Campo personalizzato per checkbox multiple"""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class FormCooperativa(FlaskForm):
    """
    Form 1: Collabora con Noi (Cooperativa)
    Acquisizione contatti da altre cooperative o partner
    """
    ragione_sociale = StringField(
        'Ragione Sociale *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Nome della vostra cooperativa/azienda'}
    )
    
    referente = StringField(
        'Referente *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Nome e cognome del referente'}
    )
    
    email = StringField(
        'Email *',
        validators=[DataRequired(message='Campo obbligatorio'), Email(message='Email non valida'), Length(max=120)],
        render_kw={'class': 'form-control', 'placeholder': 'email@esempio.it'}
    )
    
    telefono = StringField(
        'Telefono',
        validators=[Optional(), Length(max=20)],
        render_kw={'class': 'form-control', 'placeholder': '+39 123 456 7890'}
    )
    
    settore = StringField(
        'Settore',
        validators=[Optional(), Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Es. Pesca, Acquacoltura, Distribuzione'}
    )
    
    messaggio = TextAreaField(
        'Messaggio',
        validators=[Optional()],
        render_kw={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrivi la tua proposta di collaborazione...'}
    )
    
    privacy_accepted = BooleanField(
        'Accetto il trattamento dei dati personali secondo la Privacy Policy *',
        validators=[DataRequired(message='Devi accettare la privacy policy')],
        render_kw={'class': 'form-check-input'}
    )

class FormCompratore(FlaskForm):
    """
    Form 2: Area Compratori (Agenti)
    Acquisizione contatti da GDO, ristoratori, grossisti, agenti
    """
    ragione_sociale = StringField(
        'Ragione Sociale *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Nome della vostra azienda'}
    )
    
    partita_iva = StringField(
        'Partita IVA',
        validators=[Optional(), Length(max=20)],
        render_kw={'class': 'form-control', 'placeholder': 'IT12345678901'}
    )
    
    referente_acquisti = StringField(
        'Referente Acquisti *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Nome e cognome del responsabile acquisti'}
    )
    
    email = StringField(
        'Email *',
        validators=[DataRequired(message='Campo obbligatorio'), Email(message='Email non valida'), Length(max=120)],
        render_kw={'class': 'form-control', 'placeholder': 'acquisti@esempio.it'}
    )
    
    telefono = StringField(
        'Telefono',
        validators=[Optional(), Length(max=20)],
        render_kw={'class': 'form-control', 'placeholder': '+39 123 456 7890'}
    )
    
    tipologia_attivita = SelectField(
        'Tipologia Attività *',
        validators=[DataRequired(message='Campo obbligatorio')],
        choices=[
            ('', 'Seleziona tipologia...'),
            ('ristorante', 'Ristorante'),
            ('gdo', 'Grande Distribuzione Organizzata'),
            ('grossista', 'Grossista'),
            ('agente', 'Agente di Vendita'),
            ('mercato', 'Mercato Ittico'),
            ('altro', 'Altro')
        ],
        render_kw={'class': 'form-select'}
    )
    
    prodotti_interesse = MultiCheckboxField(
        'Prodotti di Interesse',
        choices=[
            ('cozze', 'Cozze'),
            ('vongole', 'Vongole'),
            ('ostriche', 'Ostriche'),
            ('capesante', 'Capesante'),
            ('altri_molluschi', 'Altri Molluschi')
        ],
        validators=[Optional()]
    )
    
    messaggio = TextAreaField(
        'Messaggio',
        validators=[Optional()],
        render_kw={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrivi le tue esigenze di acquisto...'}
    )
    
    privacy_accepted = BooleanField(
        'Accetto il trattamento dei dati personali secondo la Privacy Policy *',
        validators=[DataRequired(message='Devi accettare la privacy policy')],
        render_kw={'class': 'form-check-input'}
    )

class FormGenerico(FlaskForm):
    """
    Form 3: Contatti Generali
    Richieste generiche
    """
    nome_cognome = StringField(
        'Nome e Cognome *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=100)],
        render_kw={'class': 'form-control', 'placeholder': 'Il tuo nome e cognome'}
    )
    
    email = StringField(
        'Email *',
        validators=[DataRequired(message='Campo obbligatorio'), Email(message='Email non valida'), Length(max=120)],
        render_kw={'class': 'form-control', 'placeholder': 'tua@email.it'}
    )
    
    oggetto = StringField(
        'Oggetto *',
        validators=[DataRequired(message='Campo obbligatorio'), Length(max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Oggetto del messaggio'}
    )
    
    messaggio = TextAreaField(
        'Messaggio *',
        validators=[DataRequired(message='Campo obbligatorio')],
        render_kw={'class': 'form-control', 'rows': 5, 'placeholder': 'Scrivi qui il tuo messaggio...'}
    )
    
    privacy_accepted = BooleanField(
        'Accetto il trattamento dei dati personali secondo la Privacy Policy *',
        validators=[DataRequired(message='Devi accettare la privacy policy')],
        render_kw={'class': 'form-check-input'}
    )