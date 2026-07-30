from flask import Blueprint

operations = Blueprint(
    "operations",
    __name__,
    template_folder="../templates"
)

from . import routes