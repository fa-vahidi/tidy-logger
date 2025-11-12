import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    from .formatters import ColoredIndentedMessageFormatter, IndentedMessageFormatter
except ImportError:
    from formatters import ColoredIndentedMessageFormatter, IndentedMessageFormatter


class TidyLogger:

    DEFAULT_FILE_NAME: str = "log"
    DEFAULT_FILE_EXTENSION: str = ".log"

    def __init__(
        self,
        file_name: None | str | Path = None,
        file_mode: str = "a",
        console_level: int | str = logging.INFO,
        file_level: int | str = logging.DEBUG,
        name: None | str = None,
        add_date_suffix_to_file_name: bool = True,
        use_file_rotation: bool = False,
        max_bytes: int = 100 * 1024 * 1024,
        backup_count: int = 10,
    ):
        """
        Initialize the TidyLogger.
        :param file_name: Name of the log file. If None, a default name with the current date is used.
        :param file_mode: Mode to open the log file ('a' for append, 'w' for write).
        :param console_level: Logging level for console output. Default is INFO.
        :param file_level: Logging level for file output. Default is DEBUG.
        :param name: Name of the logger. If None, the class name is used.
        :param add_date_suffix_to_file_name: Whether to append the current date to the log file name.
        :param use_file_rotation: Whether to use rotating file handler.
        :param max_bytes: Maximum size in bytes for the log file before rotation (only if use_file_rotation is True).
        :param backup_count: Number of backup files to keep (only if use_file_rotation is True).
        """
        self.logger = logging.getLogger(self.__class__.__name__ if name is None else name)
        self.logger.setLevel(min(console_level, file_level))

        file_formatter = IndentedMessageFormatter()
        console_formatter = ColoredIndentedMessageFormatter()

        # Avoid adding handlers if they already exist (prevents duplicate logs)
        if not self.logger.handlers:

            # File handler
            file_path: Path = self._create_file_path(file_name, add_date_suffix_to_file_name=add_date_suffix_to_file_name)

            file_path.parent.mkdir(parents=True, exist_ok=True)

            if use_file_rotation:
                file_handler = RotatingFileHandler(filename=file_path, mode=file_mode, maxBytes=max_bytes, backupCount=backup_count)
            else:
                file_handler = logging.FileHandler(filename=file_path, mode=file_mode)

            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(file_level)
            self.logger.addHandler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(console_level)
            self.logger.addHandler(console_handler)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Log a debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Log an info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Log a warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Log an error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Log a critical message."""
        self.logger.critical(message, *args, **kwargs)

    def close(self) -> None:
        """Close all handlers associated with the logger."""
        for handler in list(self.logger.handlers):
            try:
                handler.flush()
            except Exception:
                pass
            try:
                handler.close()
            except Exception:
                pass
            self.logger.removeHandler(handler)

    @staticmethod
    def _create_file_path(file_name: None | str | Path, add_date_suffix_to_file_name: bool = True) -> Path:
        """
        Validate and normalize a log file path.
        Adds '.log' extension if missing.
        :param file_name: The input file name.
        :param add_date_suffix_to_file_name: Whether to append the current date to the log file name.
        :return: A Path object representing the validated log file path.
        :raises ValueError: If the file name is not null and empty, and if it is invalid.
        """

        date_suffix: str = datetime.now().strftime("%Y%m%d")

        if file_name is None and add_date_suffix_to_file_name:
            return Path("{}_{}{}".format(TidyLogger.DEFAULT_FILE_NAME, date_suffix, TidyLogger.DEFAULT_FILE_EXTENSION))
        elif file_name is None:
            return Path("{}{}".format(TidyLogger.DEFAULT_FILE_NAME, TidyLogger.DEFAULT_FILE_EXTENSION))

        if isinstance(file_name, (str, Path)):
            p = Path(file_name)
            s = str(p)

            if not s.strip():
                raise ValueError("`file_name` cannot be empty.")
            if "\0" in s:
                raise ValueError("`file_name` contains null byte.")

            if os.name == "nt":
                invalid_chars = set(r'<>:"/\\|?*')
                if any(ch in s for ch in invalid_chars):
                    raise ValueError("`file_name` contains invalid characters for Windows paths.")
                reserved = {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
                for part in p.parts:
                    if Path(part).stem.upper() in reserved:
                        raise ValueError("`file_name` path contains reserved Windows device name component.")

            if add_date_suffix_to_file_name:
                suffix = p.suffix if p.suffix else TidyLogger.DEFAULT_FILE_EXTENSION
                new_name = f"{p.stem}_{date_suffix}{suffix}"
                p = p.with_name(new_name)
            else:
                if p.suffix == "":
                    p = p.with_suffix(TidyLogger.DEFAULT_FILE_EXTENSION)

            return p

        raise ValueError("'file_name' should be of type 'str', 'Path', or 'None'.")
