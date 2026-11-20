"""
Routes per l'area amministrativa (CMS)
Gestisce autenticazione, impostazioni globali e gestione contenuti
"""
import os
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin import bp
from app.models import User, GlobalSettings, ContentCard, LeadCooperativa, LeadCompratore, LeadGenerico
from app.admin.forms import LoginForm, GlobalSettingsForm, ContentCardForm
from app import db

def allowed_file(filename):
    """Verifica se il file ha un'estensione consentita"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login amministratore"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login effettuato con successo!', 'success')
            
            # Redirect alla pagina richiesta o dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
        else:
            flash('Username o password non validi.', 'error')
    
    return render_template('admin/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    """Logout amministratore"""
    logout_user()
    flash('Logout effettuato con successo.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard amministrativa"""
    # Statistiche rapide
    stats = {
        'lead_cooperativa': LeadCooperativa.query.count(),
        'lead_compratore': LeadCompratore.query.count(),
        'lead_generico': LeadGenerico.query.count(),
        'content_cards': ContentCard.query.filter_by(is_active=True).count()
    }
    
    # Ultimi lead ricevuti
    recent_leads = {
        'cooperativa': LeadCooperativa.query.order_by(LeadCooperativa.created_at.desc()).limit(5).all(),
        'compratore': LeadCompratore.query.order_by(LeadCompratore.created_at.desc()).limit(5).all(),
        'generico': LeadGenerico.query.order_by(LeadGenerico.created_at.desc()).limit(5).all()
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_leads=recent_leads)

@bp.route('/impostazioni-sito', methods=['GET', 'POST'])
@login_required
def impostazioni_sito():
    """
    Gestione Identità Globale (Modello: GlobalSettings)
    Modifica dell'unica riga della tabella GlobalSettings
    """
    settings = GlobalSettings.query.first()
    if not settings:
        # Crea impostazioni di default se non esistono
        settings = GlobalSettings(partita_iva='')
        db.session.add(settings)
        db.session.commit()
    
    form = GlobalSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        # Gestione upload logo
        if form.logo.data and form.logo.data.filename:
            if allowed_file(form.logo.data.filename):
                try:
                    # Elimina il logo precedente se esiste
                    if settings.logo_filename:
                        old_logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], settings.logo_filename)
                        if os.path.exists(old_logo_path):
                            os.remove(old_logo_path)
                    
                    # Crea nuovo nome file con timestamp
                    import time
                    timestamp = str(int(time.time()))
                    original_filename = secure_filename(form.logo.data.filename)
                    name, ext = os.path.splitext(original_filename)
                    filename = f"logo_{timestamp}{ext}"
                    
                    logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.logo.data.save(logo_path)
                    settings.logo_filename = filename
                except Exception as e:
                    current_app.logger.error(f'Errore upload logo: {e}')
                    flash('Errore durante il caricamento del logo.', 'error')
                    return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
            else:
                flash(f'Formato file logo non supportato. Formati consentiti: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'error')
                return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
        
        # Gestione upload favicon
        if form.favicon.data and form.favicon.data.filename:
            if allowed_file(form.favicon.data.filename):
                try:
                    # Elimina il favicon precedente se esiste
                    if settings.favicon_filename:
                        old_favicon_path = os.path.join(current_app.config['UPLOAD_FOLDER'], settings.favicon_filename)
                        if os.path.exists(old_favicon_path):
                            os.remove(old_favicon_path)
                    
                    # Crea nuovo nome file con timestamp
                    import time
                    timestamp = str(int(time.time()))
                    original_filename = secure_filename(form.favicon.data.filename)
                    name, ext = os.path.splitext(original_filename)
                    filename = f"favicon_{timestamp}{ext}"
                    
                    favicon_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.favicon.data.save(favicon_path)
                    settings.favicon_filename = filename
                except Exception as e:
                    current_app.logger.error(f'Errore upload favicon: {e}')
                    flash('Errore durante il caricamento del favicon.', 'error')
                    return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
            else:
                flash(f'Formato file favicon non supportato. Formati consentiti: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'error')
                return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
        
        # Gestione upload sfondo homepage
        if form.sfondo_homepage.data and form.sfondo_homepage.data.filename:
            if allowed_file(form.sfondo_homepage.data.filename):
                try:
                    # Elimina lo sfondo precedente se esiste
                    if settings.sfondo_homepage_filename:
                        old_sfondo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], settings.sfondo_homepage_filename)
                        if os.path.exists(old_sfondo_path):
                            os.remove(old_sfondo_path)
                    
                    # Crea nuovo nome file con timestamp
                    import time
                    timestamp = str(int(time.time()))
                    original_filename = secure_filename(form.sfondo_homepage.data.filename)
                    name, ext = os.path.splitext(original_filename)
                    filename = f"sfondo_homepage_{timestamp}{ext}"
                    
                    sfondo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.sfondo_homepage.data.save(sfondo_path)
                    settings.sfondo_homepage_filename = filename
                except Exception as e:
                    current_app.logger.error(f'Errore upload sfondo homepage: {e}')
                    flash('Errore durante il caricamento dello sfondo homepage.', 'error')
                    return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
            else:
                flash(f'Formato file sfondo non supportato. Formati consentiti: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'error')
                return render_template('admin/impostazioni_sito.html', form=form, settings=settings)
        
        # Aggiorna altri campi
        settings.nome_sito = form.nome_sito.data
        settings.titolo_homepage = form.titolo_homepage.data
        settings.sottotitolo_homepage = form.sottotitolo_homepage.data
        settings.partita_iva = form.partita_iva.data
        settings.anno_fondazione = form.anno_fondazione.data
        settings.colophon = form.colophon.data
        settings.facebook_url = form.facebook_url.data
        settings.instagram_url = form.instagram_url.data
        settings.linkedin_url = form.linkedin_url.data
        
        try:
            db.session.commit()
            flash('Impostazioni aggiornate con successo!', 'success')
            return redirect(url_for('admin.impostazioni_sito'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore aggiornamento impostazioni: {e}')
            flash('Errore durante il salvataggio.', 'error')
    
    return render_template('admin/impostazioni_sito.html', form=form, settings=settings)

@bp.route('/gestione-contenuti')
@login_required
def gestione_contenuti():
    """
    Gestione Contenuti a "Card" (Modello: ContentCard)
    Elenco di tutte le card create, filtrabili per sezione
    """
    sezione = request.args.get('sezione', '')
    
    query = ContentCard.query
    if sezione:
        query = query.filter_by(sezione=sezione)
    
    cards = query.order_by(ContentCard.sezione.asc(), ContentCard.ordine.asc()).all()
    
    # Sezioni disponibili
    sezioni = db.session.query(ContentCard.sezione).distinct().all()
    sezioni = [s[0] for s in sezioni]
    
    return render_template('admin/gestione_contenuti.html', cards=cards, sezioni=sezioni, sezione_filtro=sezione)

@bp.route('/gestione-contenuti/nuovo', methods=['GET', 'POST'])
@login_required
def nuovo_contenuto():
    """Crea una nuova ContentCard"""
    form = ContentCardForm()
    
    if form.validate_on_submit():
        card = ContentCard(
            titolo=form.titolo.data,
            contenuto=form.contenuto.data,
            sezione=form.sezione.data,
            ordine=form.ordine.data,
            is_active=form.is_active.data
        )
        
        # Gestione upload immagine
        if form.immagine.data and form.immagine.data.filename:
            if allowed_file(form.immagine.data.filename):
                try:
                    filename = secure_filename(form.immagine.data.filename)
                    # Aggiungi timestamp per evitare conflitti di nome
                    import time
                    timestamp = str(int(time.time()))
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{timestamp}{ext}"
                    
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.immagine.data.save(image_path)
                    card.immagine_filename = filename
                except Exception as e:
                    current_app.logger.error(f'Errore upload immagine: {e}')
                    flash('Errore durante il caricamento dell\'immagine.', 'error')
                    return render_template('admin/form_contenuto.html', form=form, title='Nuovo Contenuto')
            else:
                flash(f'Formato file non supportato. Formati consentiti: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'error')
                return render_template('admin/form_contenuto.html', form=form, title='Nuovo Contenuto')
        
        try:
            db.session.add(card)
            db.session.commit()
            flash('Contenuto creato con successo!', 'success')
            return redirect(url_for('admin.gestione_contenuti'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore creazione contenuto: {e}')
            flash('Errore durante il salvataggio.', 'error')
    
    return render_template('admin/form_contenuto.html', form=form, title='Nuovo Contenuto')

@bp.route('/gestione-contenuti/modifica/<int:id>', methods=['GET', 'POST'])
@login_required
def modifica_contenuto(id):
    """Modifica una ContentCard esistente"""
    card = ContentCard.query.get_or_404(id)
    form = ContentCardForm(obj=card)
    
    if form.validate_on_submit():
        card.titolo = form.titolo.data
        card.contenuto = form.contenuto.data
        card.sezione = form.sezione.data
        card.ordine = form.ordine.data
        card.is_active = form.is_active.data
        
        # Gestione upload immagine
        if form.immagine.data and form.immagine.data.filename:
            if allowed_file(form.immagine.data.filename):
                try:
                    filename = secure_filename(form.immagine.data.filename)
                    # Aggiungi timestamp per evitare conflitti di nome
                    import time
                    timestamp = str(int(time.time()))
                    name, ext = os.path.splitext(filename)
                    filename = f"{name}_{timestamp}{ext}"
                    
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    form.immagine.data.save(image_path)
                    card.immagine_filename = filename
                except Exception as e:
                    current_app.logger.error(f'Errore upload immagine: {e}')
                    flash('Errore durante il caricamento dell\'immagine.', 'error')
                    return render_template('admin/form_contenuto.html', form=form, title='Modifica Contenuto', card=card)
            else:
                flash(f'Formato file non supportato. Formati consentiti: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}', 'error')
                return render_template('admin/form_contenuto.html', form=form, title='Modifica Contenuto', card=card)
        
        try:
            db.session.commit()
            flash('Contenuto aggiornato con successo!', 'success')
            return redirect(url_for('admin.gestione_contenuti'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Errore aggiornamento contenuto: {e}')
            flash('Errore durante il salvataggio.', 'error')
    
    return render_template('admin/form_contenuto.html', form=form, title='Modifica Contenuto', card=card)

@bp.route('/gestione-contenuti/elimina/<int:id>', methods=['POST'])
@login_required
def elimina_contenuto(id):
    """Elimina una ContentCard"""
    card = ContentCard.query.get_or_404(id)
    
    try:
        db.session.delete(card)
        db.session.commit()
        flash('Contenuto eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Errore eliminazione contenuto: {e}')
        flash('Errore durante l\'eliminazione.', 'error')
    
    return redirect(url_for('admin.gestione_contenuti'))

# Routes per la consultazione dei lead

@bp.route('/lead-cooperativa')
@login_required
def lead_cooperativa():
    """Consultazione lead cooperativa"""
    leads = LeadCooperativa.query.order_by(LeadCooperativa.created_at.desc()).all()
    return render_template('admin/lead_cooperativa.html', leads=leads)

@bp.route('/lead-compratore')
@login_required
def lead_compratore():
    """Consultazione lead compratore"""
    leads = LeadCompratore.query.order_by(LeadCompratore.created_at.desc()).all()
    return render_template('admin/lead_compratore.html', leads=leads)

@bp.route('/lead-generico')
@login_required
def lead_generico():
    """Consultazione lead generico"""
    leads = LeadGenerico.query.order_by(LeadGenerico.created_at.desc()).all()
    return render_template('admin/lead_generico.html', leads=leads)

# Routes per eliminazione lead

@bp.route('/lead-cooperativa/elimina/<int:id>', methods=['POST'])
@login_required
def elimina_lead_cooperativa(id):
    """Elimina un lead cooperativa"""
    lead = LeadCooperativa.query.get_or_404(id)
    
    try:
        db.session.delete(lead)
        db.session.commit()
        flash('Lead cooperativa eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Errore eliminazione lead cooperativa: {e}')
        flash('Errore durante l\'eliminazione.', 'error')
    
    return redirect(url_for('admin.lead_cooperativa'))

@bp.route('/lead-compratore/elimina/<int:id>', methods=['POST'])
@login_required
def elimina_lead_compratore(id):
    """Elimina un lead compratore"""
    lead = LeadCompratore.query.get_or_404(id)
    
    try:
        db.session.delete(lead)
        db.session.commit()
        flash('Lead compratore eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Errore eliminazione lead compratore: {e}')
        flash('Errore durante l\'eliminazione.', 'error')
    
    return redirect(url_for('admin.lead_compratore'))

@bp.route('/lead-generico/elimina/<int:id>', methods=['POST'])
@login_required
def elimina_lead_generico(id):
    """Elimina un lead generico"""
    lead = LeadGenerico.query.get_or_404(id)
    
    try:
        db.session.delete(lead)
        db.session.commit()
        flash('Lead generico eliminato con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Errore eliminazione lead generico: {e}')
        flash('Errore durante l\'eliminazione.', 'error')
    
    return redirect(url_for('admin.lead_generico'))