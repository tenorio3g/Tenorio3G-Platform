class Tenorio3GException(Exception):
    """
    Excepción base para toda la plataforma.
    """

    def __init__(self, message="Ha ocurrido un error en Tenorio3G Platform."):
        super().__init__(message)