from __future__ import print_function

from flask import Blueprint
from config import Config

from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER