import logging
import os
from datetime import datetime

class LoggerManager:
    _logger = None

    @staticmethod
    def get_logger(nombre="app"):
        if LoggerManager._logger is None:
            LoggerManager._logger = logging.getLogger(nombre)
            LoggerManager._logger.setLevel(logging.DEBUG)

            # Crear carpeta de logs si no existe
            os.makedirs("logs", exist_ok=True)
            fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_path = os.path.join("logs", f"{nombre}_{fecha_hora}.log")

            # Formato
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

            # Archivo
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            LoggerManager._logger.addHandler(file_handler)

            # Consola (opcional)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            LoggerManager._logger.addHandler(console_handler)

        return LoggerManager._logger
