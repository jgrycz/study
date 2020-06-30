from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from app.models import Permission


@main.app_context_processor
def injection_premissions():
    return dict(Permission=Permission)
