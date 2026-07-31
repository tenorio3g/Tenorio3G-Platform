"""
====================================================

Tenorio3G Platform

Assets Domain

Asset Business Model

Author:
Ingeniero Fortunato Tenorio
Arquitecto

====================================================
"""


class Asset:

    """
    Representa un activo de la organización.

    Un activo conserva su identidad durante toda
    su vida y genera conocimiento cada vez que
    ocurre una intervención.
    """

    def __init__(self):

        # ADN DEL ACTIVO

        self.identity = None

        self.location = None

        self.operational_status = None

        self.safety = None

        self.technical_data = None

        self.history = None

        self.knowledge = None

        self.lifecycle = None