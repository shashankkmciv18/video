import logging
import os
from logging.handlers import RotatingFileHandler


class CentralizedLogger:
    _instance = None

    @staticmethod
    def get_logger(name="ApplicationLogger"):
        if CentralizedLogger._instance is None:
            CentralizedLogger(name)
        return CentralizedLogger._instance

    def __init__(self, name):
        if CentralizedLogger._instance is not None:
            raise Exception("This class is a singleton!")
        CentralizedLogger._instance = self

        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "application.log"), maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
