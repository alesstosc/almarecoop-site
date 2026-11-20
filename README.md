# Sito istituzionale + CMS — Cooperativa Mitilicoltori di Comacchio

Applicazione web completa (sito pubblico **+** pannello di amministrazione) sviluppata in
**Python/Flask** per una cooperativa ittica, con CMS per la gestione autonoma dei contenuti e
raccolta di contatti B2B. **In produzione.**

> Questo repository contiene **solo il codice applicativo**.
> Database di produzione, file caricati dagli utenti e variabili d'ambiente **non sono
> versionati**: sono artefatti di runtime, e contengono dati personali.

---

## Cosa fa

**Sito pubblico**
- Home con contenuti gestibili, pagine *Chi siamo*, *Prodotti*, *News*
- Tre moduli di contatto differenziati: collaborazione, area compratori, contatti generici
- Informativa privacy e raccolta del consenso esplicito su ogni form (Reg. UE 2016/679)

**Pannello di amministrazione** (area riservata, autenticazione richiesta)
- Dashboard e gestione contenuti (creazione, modifica, attivazione, ordinamento)
- Impostazioni globali del sito: logo, favicon, testi della home, colophon, contatti social
- Consultazione dei lead raccolti, suddivisi per tipologia
- Upload di immagini con validazione dell'estensione

---

## Stack

| Livello | Tecnologia |
|---|---|
| Linguaggio | Python 3.12 |
| Framework | Flask 2.3 (application factory + Blueprint) |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Database | SQLite in sviluppo — PostgreSQL come alternativa scalabile |
| Form | Flask-WTF / WTForms con protezione CSRF |
| Autenticazione | Flask-Login + hash delle password con Werkzeug |
| Frontend | Template Jinja2 + Bootstrap 5 |
| Immagini | Pillow |
| Deploy | Container Docker su VPS cloud, TLS con Let's Encrypt |

---

## Architettura

```
almarecoop-site/
├── app/
│   ├── __init__.py          # application factory, registrazione blueprint ed estensioni
│   ├── models.py            # User, GlobalSettings, ContentCard, LeadCooperativa,
│   │                        # LeadCompratore, LeadGenerico
│   ├── main/                # Blueprint pubblico
│   │   ├── routes.py        # viste del sito
│   │   └── forms.py         # form WTForms + validazione
│   ├── admin/               # Blueprint area riservata (login obbligatorio)
│   │   ├── routes.py        # CRUD contenuti, impostazioni, lead
│   │   └── forms.py
│   ├── templates/           # Jinja2, layout separati per pubblico e admin
│   └── static/              # asset statici (gli upload finiscono qui a runtime)
├── config.py                # configurazione da variabili d'ambiente
├── dbinit.py                # inizializzazione DB + primo utente admin (password chiesta a terminale)
├── run.py                   # avvio in sviluppo
└── requirements.txt
```

Separazione netta dei ruoli: **`main`** (pubblico, sola lettura) e **`admin`** (autenticato,
scrittura). Le impostazioni del sito vivono su database, non hardcoded nei template: il cliente
può cambiare logo, testi e contatti senza toccare il codice.

---

## Sicurezza e conformità

Scelte adottate e verificabili nel codice:

- **Nessun segreto nel repository.** `SECRET_KEY` e credenziali SMTP arrivano da variabili
  d'ambiente; se `SECRET_KEY` manca, l'applicazione **si rifiuta di partire** (nessun valore di
  fallback insicuro).
- **Password mai in chiaro**: hash Werkzeug, e `dbinit.py` chiede la password dell'amministratore
  a terminale con `getpass`.
- **CSRF** su tutti i form (Flask-WTF), **sessioni** gestite da Flask-Login.
- **Upload**: whitelist delle estensioni, limite di dimensione della richiesta (16 MB).
- **Dati personali fuori dal versionamento** (`.gitignore`): il database di produzione e i file
  caricati non finiscono mai in un commit.
- **GDPR**: consenso esplicito e tracciato sui form, informativa estesa e cookie policy.

---

## Avvio in locale

```bash
git clone <url-di-questo-repo>
cd almarecoop-site

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# inserisci una SECRET_KEY generata con:
#   python -c "import secrets; print(secrets.token_hex(32))"

python dbinit.py                   # crea il DB e l'utente amministratore (password richiesta)
python run.py                      # http://127.0.0.1:5000
```

### Variabili d'ambiente

| Variabile | Obbligatoria | Descrizione |
|---|---|---|
| `SECRET_KEY` | **sì** | chiave di firma delle sessioni; senza, l'app non parte |
| `DATABASE_URL` | no | default SQLite in `instance/database.db` |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS` | no | SMTP per le notifiche dei form |
| `MAIL_USERNAME`, `MAIL_PASSWORD` | no | credenziali SMTP |
| `ADMIN_EMAIL` | no | destinatario delle notifiche |
| `FLASK_DEBUG` | no | `1` abilita il debug server, **solo in locale** |

---

## Deploy

In produzione l'applicazione **non** viene avviata con `run.py` (che è pensato per lo sviluppo):
gira su un application server WSGI dietro reverse proxy con terminazione TLS, e i certificati
sono rinnovati automaticamente con Certbot / Let's Encrypt. Il database e la directory degli
upload sono volumi persistenti, mai parte dell'immagine.

---

## Note di progetto

- Il pannello admin è stato progettato perché il personale della cooperativa fosse autonomo sui
  contenuti, senza intervento tecnico per modificare testi, immagini o recapiti.
- I tre form sono differenziati per **qualificare il lead** (B2B, fornitori, generico) e ridurre
  il rumore in fase di consultazione.
- Il repository pubblico è una versione ripulita del progetto reale: storia Git riscritta,
  dati di produzione rimossi, segreti esternalizzati.

---

## Autore

Sviluppo, amministrazione e messa in produzione: **Alessandro Toscani**
— [almarecoop.it](https://almarecoop.it)
