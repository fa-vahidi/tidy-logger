import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import platformdirs

try:
    from .formatters import ColoredIndentedMessageFormatter, IndentedMessageFormatter
except ImportError:
    from formatters import ColoredIndentedMessageFormatter, IndentedMessageFormatter


class TidyLogger:

    DEFAULT_FILE_NAME: str = "log"
    DEFAULT_FILE_EXTENSION: str = ".log"
    TIDY_LOGGER_LOG_FILE_DIR_ENV_VAR: str = "TIDY_LOGGER_LOG_FILE_DIR"
    TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR: str = "TIDY_LOGGER_LOG_FILE_NAME"

    def __init__(
        self,
        app_name: str | None = None,
        app_author: str | None = None,
        log_file_name: str | None = None,
        log_file_directory: str | Path | None = None,
        file_mode: str = "a",
        console_level: int | str = logging.INFO,
        file_level: int | str = logging.DEBUG,
        add_date_suffix_to_file_name: bool = True,
        print_log_file_path: bool = True,
        use_file_rotation: bool = False,
        max_bytes: int = 100 * 1024 * 1024,
        backup_count: int = 10,
    ):
        """
        Initialize the TidyLogger.
        :param app_name: Name of the application (used for creating the default log directory). If specified, cannot be an empty string.
        :param app_author: Author (or company) of the application (used for creating the default log directory on some platforms). If specified, cannot be an empty string.
        :param log_file_name: Name of the log file. If None, first checks for environment variable value, then a default name with the current date is used. if specified, cannot be an empty string.
        :param log_file_directory: Directory to store the log file. If None, first checks for environment variable value, then uses platform-specific user log directory. If specified, cannot be an empty string.
        :param file_mode: Mode to open the log file ('a' for append, 'w' for write).
        :param console_level: Logging level for console output. Default is INFO.
        :param file_level: Logging level for file output. Default is DEBUG.
        :param add_date_suffix_to_file_name: Whether to append the current date to the log file name.
        :param print_log_file_path: Whether to print the log file path to the console upon initialization, or not.
        :param use_file_rotation: Whether to use rotating file handler.
        :param max_bytes: Maximum size in bytes for the log file before rotation (only if use_file_rotation is True).
        :param backup_count: Number of backup files to keep (only if use_file_rotation is True).
        :raises ValueError: if any of the following arguments are empty strings: `app_name`, `app_author`, `file_name`, `file_directory`.
        """

        if app_name == "":
            raise ValueError("`app_name` cannot be an empty string.")
        if app_author == "":
            raise ValueError("`app_author` cannot be an empty string.")
        if log_file_name == "":
            raise ValueError("`log_file_name` cannot be an empty string.")
        if log_file_directory == "":
            raise ValueError("`log_file_directory` cannot be an empty string.")

        resolved_log_file_directory: Path = self._create_log_file_directory(
            log_file_directory=log_file_directory, log_file_directory_environment_variable_name=self.TIDY_LOGGER_LOG_FILE_DIR_ENV_VAR, app_name=app_name, app_author=app_author
        )

        resolved_log_file_name: Path = self._create_log_file_name(
            log_file_name=log_file_name, log_file_name_environment_variable_name=self.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR, add_date_suffix_to_file_name=add_date_suffix_to_file_name
        )

        log_file_path: Path = resolved_log_file_directory / resolved_log_file_name

        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.__class__.__name__ if app_name is None else app_name)
        self.logger.setLevel(min(console_level, file_level))

        file_formatter = IndentedMessageFormatter()
        console_formatter = ColoredIndentedMessageFormatter()

        # Avoid adding handlers if they already exist (prevents duplicate logs)
        if not self.logger.handlers:

            if use_file_rotation:
                file_handler = RotatingFileHandler(filename=log_file_path, mode=file_mode, maxBytes=max_bytes, backupCount=backup_count)
            else:
                file_handler = logging.FileHandler(filename=log_file_path, mode=file_mode)

            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(file_level)
            self.logger.addHandler(file_handler)

            if print_log_file_path:
                print("Log file path:", log_file_path)
                print()

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(console_level)
            self.logger.addHandler(console_handler)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Log a debug message."""
        kwargs.setdefault("stacklevel", 2)
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Log an info message."""
        kwargs.setdefault("stacklevel", 2)
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Log a warning message."""
        kwargs.setdefault("stacklevel", 2)
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Log an error message."""
        kwargs.setdefault("stacklevel", 2)
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Log a critical message."""
        kwargs.setdefault("stacklevel", 2)
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
    def _create_log_file_directory(
        log_file_directory: str | Path | None = None,
        log_file_directory_environment_variable_name: str = TIDY_LOGGER_LOG_FILE_DIR_ENV_VAR,
        app_name: str | None = None,
        app_author: str | None = None,
        use_os_standard_log_directory: bool = True,
    ) -> Path:
        """
        Determine the log file directory based on the provided argument, environment variable, and OS standard log directory, or current working directory.
        :param log_file_directory: The log file directory. If None, checks the environment variable.
        :param log_file_directory_environment_variable_name: The name of the environment variable to check for the log file directory. if the environment variable is not set, the function will use the OS standard log directory if `use_os_standard_log_directory` is True. Otherwise, it will default to the current working directory.
        :param app_name: The name of the application (used for OS standard log directory).
        :param app_author: The author of the application (used for OS standard log directory).
        :param use_os_standard_log_directory: Whether to use the OS standard log directory if neither the argument nor the environment variable is set. Defaults to True. If False, defaults to the current working directory.
        :return: A Path object representing the log file directory.
        :raises ValueError: If the provided `log_file_directory` is an empty string, or if the environment variable is set to an empty string or points to a non-directory.
        """

        # explicit argument
        if log_file_directory is not None:
            if isinstance(log_file_directory, Path):
                p = log_file_directory
            elif isinstance(log_file_directory, str):
                if not log_file_directory.strip():
                    raise ValueError("`log_file_directory` cannot be an empty string.")
                else:
                    p = Path(log_file_directory.strip())
            else:
                raise ValueError("`log_file_directory` should be of type 'str', 'Path', or 'None'.")
            return p.expanduser().resolve()

        # environment variable
        env_value = os.getenv(log_file_directory_environment_variable_name)
        if env_value is not None:
            env_value = env_value.strip()
            if not env_value:
                raise ValueError(f"`{log_file_directory_environment_variable_name}` environment variable is set to an empty string.")
            p = Path(env_value)
            if p.exists() and not p.is_dir():
                raise ValueError(f"`{log_file_directory_environment_variable_name}` environment variable points to a non-directory: '{p}'")
            return p.expanduser().resolve()

        # OS standard log directory
        if use_os_standard_log_directory:
            if app_name is not None and app_author is not None:
                return Path(platformdirs.user_log_dir(app_name, app_author)).expanduser().resolve()

        # fallback: current working directory as absolute path
        return Path.cwd().resolve()

    @staticmethod
    def _create_log_file_name(
        log_file_name: str | None = None, log_file_name_environment_variable_name: str = TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR, add_date_suffix_to_file_name: bool = True
    ) -> Path:
        """
        Validate and normalize a log file name.
        Adds '.log' extension if missing.
        :param log_file_name: The log file name. If None, checks the environment variable, then uses the default name.
        :param log_file_name_environment_variable_name: The name of the environment variable to check for the log file name. If the log_file_name is None and the environment variable is not set, the function will use the default log file name.
        :param add_date_suffix_to_file_name: Whether to append the current date to the log file name.
        :return: A string representing the validated log file name.
        :raises ValueError: If the provided `log_file_name` is an empty string, contains null bytes, or contains invalid characters for Windows paths; or if the environment variable is set to an empty string.
        """

        date_suffix: str = datetime.now().strftime("%Y%m%d")

        if log_file_name is None:
            log_file_name_from_env: str = os.getenv(log_file_name_environment_variable_name)
            # Check environment variable for log file name
            if log_file_name_from_env is not None:
                env_value = log_file_name_from_env.strip()
                if not env_value:
                    raise ValueError(f"`{log_file_name_environment_variable_name}` environment variable is set to an empty string.")
                # Use the environment variable value as the log file name and add the date suffix
                elif add_date_suffix_to_file_name:
                    p = Path(env_value)
                    suffix = p.suffix if p.suffix else TidyLogger.DEFAULT_FILE_EXTENSION
                    new_name = f"{p.stem}_{date_suffix}{suffix}"
                    p = p.with_name(new_name)
                    return TidyLogger._validate_file_name(p)
                # Use the environment variable value as the log file name without adding the date suffix
                else:
                    p = Path(env_value)
                    if p.suffix == "":
                        p = p.with_suffix(TidyLogger.DEFAULT_FILE_EXTENSION)
                    return TidyLogger._validate_file_name(p)
            # No environment variable set, use default file name with the date suffix
            elif add_date_suffix_to_file_name:
                return Path("{}_{}{}".format(TidyLogger.DEFAULT_FILE_NAME, date_suffix, TidyLogger.DEFAULT_FILE_EXTENSION))
            # No environment variable set, use default file name without date suffix
            else:
                return Path("{}{}".format(TidyLogger.DEFAULT_FILE_NAME, TidyLogger.DEFAULT_FILE_EXTENSION))

        # Log file name provided explicitly
        if isinstance(log_file_name, str):
            log_file_name = log_file_name.strip()
            if not log_file_name:
                raise ValueError("`log_file_name` cannot be empty.")
            if "\0" in log_file_name:
                raise ValueError("`log_file_name` contains null byte.")

            p = Path(log_file_name)

            if add_date_suffix_to_file_name:
                suffix = p.suffix if p.suffix else TidyLogger.DEFAULT_FILE_EXTENSION
                new_name = f"{p.stem}_{date_suffix}{suffix}"
                p = p.with_name(new_name)
            else:
                if p.suffix == "":
                    p = p.with_suffix(TidyLogger.DEFAULT_FILE_EXTENSION)

            return TidyLogger._validate_file_name(p)

        raise ValueError("`log_file_name` should be of type 'str', or 'None'.")

    @staticmethod
    def _validate_file_name(file_name: Path) -> Path:
        """
        Validate a file name for invalid characters on Windows.
        Raises ValueError if invalid characters are found.
        :param file_name: The file name to validate.
        :return: The validated file name.
        :raises ValueError: If the file name contains invalid characters for Windows paths.
        """
        if not isinstance(file_name, (str, Path)):
            raise ValueError("`file_name` should be of type 'str' or 'Path'.")
        elif isinstance(file_name, str):
            file_name = Path(file_name)

        if os.name == "nt" and any(os.path.isreserved(part) for part in file_name.parts):
            raise ValueError("`file_name` contains reserved Windows device name component. file_name: '{}'".format(file_name))

        return file_name
