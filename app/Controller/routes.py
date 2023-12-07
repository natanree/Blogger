from flask import Blueprint
from config import Config
from flask import current_app as app
from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER