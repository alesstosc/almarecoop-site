"""
Routes per il sito pubblico della Cooperativa
Gestisce homepage, pagine informative e form di contatto
"""
from flask import render_template, request, flash, redirect, url_for, current_app
from app.main import bp
from app.models import ContentCard, LeadCooperativa, LeadCompratore, LeadGenerico
from app.main.forms import FormCooperativa, FormCompratore, FormGenerico
from app import db
import json

@bp.route('/')
def index():
    """
    Homepage con contenuti dinamici da ContentCard
    Seguendo le specifiche del paper: nessun testo statico, solo card dinamiche
    """
    # Query per ottenere tutte le ContentCard della sezione 'Homepage'
    homepage_cards = ContentCard.query.filter_by(
        sezione='Homepage', 
        is_active=True
    ).order_by(ContentCard.ordine.asc()).all()
    
    return render_template('index.html', cards=homepage_cards)

@bp.route('/chi-siamo')
def chi_siamo():
    """Pagina Chi Siamo con contenuti dinamici"""
    chi_siamo_cards = ContentCard.query.filter_by(
        sezione='Chi Siamo', 
        is_active=True
    ).order_by(ContentCard.ordine.asc()).all()
    
    return render_template('chi_siamo.html', cards=chi_siamo_cards)

@bp.route('/prodotti')
def prodotti():
    """Pagina Prodotti con contenuti dinamici"""
    prodotti_cards = ContentCard.query.filter_by(
        sezione='Prodotti', 
        is_active=True
    ).order_by(ContentCard.ordine.asc()).all()
    
    return render_template('prodotti.html', cards=prodotti_cards)

@bp.route('/news')
def news():
    """Pagina News con contenuti dinamici"""
    news_cards = ContentCard.query.filter_by(
        sezione='News', 
        is_active=True
    ).order_by(ContentCard.ordine.asc()).all()
    
    return render_template('news.html', cards=news_cards)

@bp.route('/collabora-con-noi', methods=['GET', 'POST'])
def collabora_con_noi():
    """
    Form 1: Collabora con Noi (Cooperativa)
    Acquisizione contatti da altre cooperative o partner
    """
    form = FormCooperativa()
    
    if form.validate_on_submit():
        # Salvataggio nel database
        lead = LeadCooperativa(
            ragione_sociale=form.ragione_sociale.data,
            referente=form.referente.data,
            email=form.email.data,
            telefono=form.telefono.data,
            settore=form.settore.data,
            messaggio=form.messaggio.data,
            privacy_accepted=form.privacy_accepted.data,
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(lead)
            db.session.commit()
            
            # TODO: Implementare invio email di notifica
            
            flash('Grazie per il tuo interesse! Ti contatteremo presto.', 'success')
            return redirect(url_for('main.collabora_con_noi'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore salvataggio lead cooperativa: {e}')
            flash('Si è verificato un errore. Riprova più tardi.', 'error')
    
    return render_template('forms/collabora_con_noi.html', form=form)

@bp.route('/area-compratori', methods=['GET', 'POST'])
def area_compratori():
    """
    Form 2: Area Compratori (Agenti)
    Acquisizione contatti da GDO, ristoratori, grossisti, agenti
    """
    form = FormCompratore()
    
    if form.validate_on_submit():
        # Serializza i prodotti di interesse (checkbox multiple)
        prodotti_interesse = json.dumps(form.prodotti_interesse.data) if form.prodotti_interesse.data else None
        
        # Salvataggio nel database
        lead = LeadCompratore(
            ragione_sociale=form.ragione_sociale.data,
            partita_iva=form.partita_iva.data,
            referente_acquisti=form.referente_acquisti.data,
            email=form.email.data,
            telefono=form.telefono.data,
            tipologia_attivita=form.tipologia_attivita.data,
            prodotti_interesse=prodotti_interesse,
            messaggio=form.messaggio.data,
            privacy_accepted=form.privacy_accepted.data,
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(lead)
            db.session.commit()
            
            # TODO: Implementare invio email di notifica
            
            flash('Grazie per il tuo interesse! Ti contatteremo presto.', 'success')
            return redirect(url_for('main.area_compratori'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore salvataggio lead compratore: {e}')
            flash('Si è verificato un errore. Riprova più tardi.', 'error')
    
    return render_template('forms/area_compratori.html', form=form)

@bp.route('/contatti', methods=['GET', 'POST'])
def contatti():
    """
    Form 3: Contatti Generali
    Richieste generiche
    """
    form = FormGenerico()
    
    if form.validate_on_submit():
        # Salvataggio nel database
        lead = LeadGenerico(
            nome_cognome=form.nome_cognome.data,
            email=form.email.data,
            oggetto=form.oggetto.data,
            messaggio=form.messaggio.data,
            privacy_accepted=form.privacy_accepted.data,
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(lead)
            db.session.commit()
            
            # TODO: Implementare invio email di notifica
            
            flash('Grazie per il tuo messaggio! Ti risponderemo presto.', 'success')
            return redirect(url_for('main.contatti'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore salvataggio lead generico: {e}')
            flash('Si è verificato un errore. Riprova più tardi.', 'error')
    
    return render_template('forms/contatti.html', form=form)

@bp.route('/privacy-policy')
def privacy_policy():
    """Pagina Privacy Policy"""
    return render_template('privacy_policy.html')

@bp.route('/favicon.ico')
def favicon():
    """Serve il favicon dinamico dalle impostazioni"""
    from flask import send_from_directory, current_app
    from app.models import GlobalSettings
    
    settings = GlobalSettings.query.first()
    if settings and settings.favicon_filename:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], settings.favicon_filename)
    else:
        # Favicon di default se non impostato
        return send_from_directory(current_app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/@vite/client')
@bp.route('/@vite/<path:filename>')
def vite_client(filename=None):
    """Gestisce richieste Vite indesiderate per evitare errori 404"""
    # Restituisce 204 No Content invece di 404 per ridurre il rumore nei log
    return '', 204

@bp.route('/node_modules/<path:filename>')
@bp.route('/src/<path:filename>')
@bp.route('/.vite/<path:filename>')
def dev_assets(filename):
    """Gestisce altre richieste di sviluppo frontend per evitare errori 404"""
    # Restituisce 204 No Content per richieste di asset di sviluppo
    return '', 204