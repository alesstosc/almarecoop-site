"""
Blueprint per l'area amministrativa (CMS)
Gestisce autenticazione, impostazioni globali e gestione contenuti
"""
from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes