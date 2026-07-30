from flask import Blueprint

assets = Blueprint(
    "assets",
    __name__,
    template_folder="../templates"
)

from . import routes