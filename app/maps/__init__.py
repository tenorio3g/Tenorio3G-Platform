from flask import Blueprint



maps = Blueprint(
    "maps",
    __name__,
    url_prefix="/maps",
    template_folder="templates",
    static_folder="static",
)


from . import routes