__all__ = ['ModuleLogger']

import logging
import os
from logging import StreamHandler
from logging.handlers import RotatingFileHandler




class ModuleLogger:
    def __init__(self,
        module_name: str,
        max_bytes: int = 5*1024*1024,
        backup_count: int = 5,
        to_console: bool = True
        ):

        self.logger = self._create_logger(
            module_name=module_name,
            max_bytes=max_bytes,
            backup_count=backup_count,
            to_console=to_console
            )

    @staticmethod
    def _create_logger(
        module_name: str,
        max_bytes: int,
        backup_count: int,
        to_console: bool
        ) -> logging.Logger:

        logger = logging.getLogger(module_name)

        level = os.getenv("LOG_LEVEL", "INFO")
        logger.setLevel(level)

        log_dir = './logs'
        log_path = os.path.join(log_dir, f"{module_name}.log")

        os.makedirs(log_dir, exist_ok=True)

        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = RotatingFileHandler(log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
            )

        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]\n\t\t\t%(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if to_console:
            console_handler = StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger
