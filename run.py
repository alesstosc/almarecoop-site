"""
Script di avvio dell'applicazione (solo sviluppo locale).

In produzione l'applicazione non va avviata con questo script ma tramite un
application server WSGI (es. gunicorn/uwsgi) dietro un reverse proxy (es. nginx),
che gestisce TLS e inoltro delle richieste.
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', '5000'))
    app.run(debug=debug, host=host, port=port)
