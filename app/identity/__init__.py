from flask import Blueprint

identity = Blueprint(
    "identity",
    __name__,
)

from . import routes