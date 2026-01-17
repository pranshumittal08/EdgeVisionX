import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class EVXLogger:
    _initialized = False
    _log_level = logging.INFO

    @classmethod
    def setup(cls, level: str = "INFO", log_dir: str = None):
        """
        Setup logging for EdgeVisionX."

        Args:
            level (str) : "DEBUG", "INFO", "WARNING", "ERROR"
            log_dir (str) : Custom log directory (default: ~/.edgevisionx/logs)
        """

        if cls._initialized:
            return

        # returns integer value for a corresponding log level such as 20 for "INFO"
        cls._log_level = getattr(logging, level.upper())

        if log_dir is None:
            log_dir = Path.home() / ".edgevisionx" / "logs"
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Root logger
        logger = logging.getLogger("edgevisionx")
        logger.setLevel(cls._log_level)
        logger.handlers.clear()

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(cls._log_level)
        console_fmt = logging.Formatter(
            f'[%(levelname)s] %(name)s: %(message)s'
        )
        console.setFormatter(console_fmt)

        # File handler with rotation
        log_file = log_dir / "edgevisionx.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*10124*1024,  # 10MB
            backupCount=3
        )
        file_handler.setLevel(cls._log_level)
        file_fmt = logging.Formatter(
            f'%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_fmt)

        logger.addHandler(console)
        logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get logger for a component"""
        if not cls._initialized:
            cls.setup()

        return logging.getLogger(f"edgevisionx.{name}")
