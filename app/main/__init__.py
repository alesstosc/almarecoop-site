"""
Blueprint per il sito pubblico della Cooperativa
Gestisce homepage, pagine informative e form di contatto
"""
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes