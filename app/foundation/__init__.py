from flask import Blueprint


foundation = Blueprint(
    "foundation",
    __name__,
    url_prefix="/foundation"
)


from app.foundation import routes