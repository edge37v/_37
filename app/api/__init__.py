from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import blog, auth, users, errors, paystack, tokens, learning