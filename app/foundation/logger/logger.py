from datetime import datetime


class Logger:
    """
    Sistema de registro de eventos de Tenorio3G Platform.
    """

    def __init__(self, module: str = "SYSTEM"):
        self.module = module

    def info(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"[INFO] {timestamp} "
            f"[{self.module}] {message}"
        )

        print(log_message)

        return log_message