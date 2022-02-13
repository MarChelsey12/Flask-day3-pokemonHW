from flask import Blueprint

bp = Blueprint('battle', __name__, url_prefix='')

from .import routes