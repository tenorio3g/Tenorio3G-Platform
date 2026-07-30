from flask import Blueprint

work_orders = Blueprint(
    "work_orders",
    __name__,
    template_folder="../templates"
)

from . import routes