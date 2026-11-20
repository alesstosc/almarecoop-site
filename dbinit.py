"""
Script di inizializzazione del database
Cooperativa Mitilicoltori Comacchio

VINCOLO OPERATIVO FONDAMENTALE (dal paper):
Questo script deve essere eseguito UNA SOLA VOLTA al setup iniziale.
Il file del database creato NON deve essere spostato, rinominato o alterato manualmente.
"""
import os
import sys
from getpass import getpass

# Aggiungi il percorso del progetto al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, GlobalSettings, ContentCard

def init_database():
    """
    Inizializza il database con:
    1. Creazione del file fisico del database
    2. Creazione di tutte le tabelle
    3. Creazione del primo utente Amministratore
    4. Popolamento della tabella GlobalSettings con P.IVA
    """
    
    print("=" * 60)
    print("INIZIALIZZAZIONE DATABASE - COOPERATIVA MITILICOLTORI")
    print("=" * 60)
    
    # Crea l'applicazione Flask
    app = create_app()
    
    with app.app_context():
        # Verifica se il database esiste già
        db_path = os.path.join(app.instance_path, 'database.db')
        
        if os.path.exists(db_path):
            print(f"⚠️  ATTENZIONE: Il database esiste già in {db_path}")
            response = input("Vuoi sovrascriverlo? (s/N): ").lower()
            if response != 's':
                print("❌ Inizializzazione annullata.")
                return False
            
            # Rimuovi il database esistente
            os.remove(db_path)
            print("🗑️  Database esistente rimosso.")
        
        # Crea la directory instance se non esiste
        os.makedirs(app.instance_path, exist_ok=True)
        
        print("📁 Creazione directory instance completata.")
        
        # Crea tutte le tabelle
        print("🔨 Creazione tabelle del database...")
        db.create_all()
        print("✅ Tabelle create con successo!")
        
        # Crea l'utente amministratore
        print("\n👤 CREAZIONE UTENTE AMMINISTRATORE")
        print("-" * 40)
        
        while True:
            username = input("Username amministratore: ").strip()
            if username:
                break
            print("❌ Username obbligatorio!")
        
        while True:
            email = input("Email amministratore: ").strip()
            if email and '@' in email:
                break
            print("❌ Email valida obbligatoria!")
        
        while True:
            password = getpass("Password amministratore: ")
            if len(password) >= 6:
                password_confirm = getpass("Conferma password: ")
                if password == password_confirm:
                    break
                else:
                    print("❌ Le password non coincidono!")
            else:
                print("❌ Password deve essere di almeno 6 caratteri!")
        
        # Crea l'utente
        admin_user = User(
            username=username,
            email=email
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        print(f"✅ Utente amministratore '{username}' creato!")
        
        # Crea le impostazioni globali
        print("\n🏢 CONFIGURAZIONE IMPOSTAZIONI GLOBALI")
        print("-" * 40)
        
        while True:
            partita_iva = input("Partita IVA della cooperativa: ").strip()
            if partita_iva:
                break
            print("❌ Partita IVA obbligatoria!")
        
        colophon_default = """Cooperativa Mitilicoltori Comacchio
Sede legale: [Inserire indirizzo]
Sede operativa: [Inserire indirizzo]
PEC: [Inserire PEC]
Telefono: [Inserire telefono]"""
        
        global_settings = GlobalSettings(
            partita_iva=partita_iva,
            colophon=colophon_default
        )
        
        db.session.add(global_settings)
        print(f"✅ Impostazioni globali create con P.IVA: {partita_iva}")
        
        # Crea alcune ContentCard di esempio per la homepage
        print("\n📄 CREAZIONE CONTENUTI DI ESEMPIO")
        print("-" * 40)
        
        sample_cards = [
            {
                'titolo': 'Benvenuti nella nostra Cooperativa',
                'contenuto': 'La Cooperativa Mitilicoltori di Comacchio rappresenta l\'eccellenza nella produzione di molluschi di alta qualità nelle acque dell\'Adriatico.',
                'sezione': 'Homepage',
                'ordine': 1
            },
            {
                'titolo': 'I nostri Prodotti',
                'contenuto': 'Cozze, vongole e altri molluschi freschi, coltivati con tecniche sostenibili e rispettose dell\'ambiente marino.',
                'sezione': 'Homepage',
                'ordine': 2
            },
            {
                'titolo': 'Qualità e Sostenibilità',
                'contenuto': 'La nostra missione è fornire prodotti di mare di altissima qualità, garantendo la sostenibilità delle nostre pratiche di allevamento.',
                'sezione': 'Homepage',
                'ordine': 3
            }
        ]
        
        for card_data in sample_cards:
            card = ContentCard(**card_data)
            db.session.add(card)
        
        print("✅ Contenuti di esempio creati per la homepage!")
        
        # Salva tutto nel database
        try:
            db.session.commit()
            print("\n🎉 INIZIALIZZAZIONE COMPLETATA CON SUCCESSO!")
            print("=" * 60)
            print(f"📍 Database creato in: {db_path}")
            print(f"👤 Admin username: {username}")
            print(f"📧 Admin email: {email}")
            print(f"🏢 P.IVA: {partita_iva}")
            print("\n🚀 Puoi ora avviare l'applicazione con: python run.py")
            print("🔐 Area admin disponibile su: http://localhost:5000/admin")
            print("=" * 60)
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERRORE durante il salvataggio: {e}")
            return False

if __name__ == '__main__':
    success = init_database()
    if not success:
        sys.exit(1)