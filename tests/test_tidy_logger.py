import logging
import os
import sys
from datetime import datetime
from os import environ
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/tidy_logger"))

from tidy_logger import TidyLogger  # noqa: E402


def test_create_log_file_name():

    date_suffix: str = datetime.now().strftime("%Y%m%d")

    # File name is None
    log_file_name: Path = TidyLogger._create_log_file_name(None)

    assert isinstance(log_file_name, Path), "File name is None: the returned file path must be a Path."

    assert log_file_name.stem[: len(TidyLogger.DEFAULT_FILE_NAME)] == TidyLogger.DEFAULT_FILE_NAME, "File name is None: the file stem must be the default file name."

    assert log_file_name.stem == "{}_{}".format(TidyLogger.DEFAULT_FILE_NAME, date_suffix), "File name is None: the file stem must contain the date suffix."

    assert log_file_name.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name is None: the file extension of must be the default extension."

    assert log_file_name.parent == Path("."), "File name is None: the parent directory must be the current directory."

    # File name is None and no date suffix
    log_file_name: Path = TidyLogger._create_log_file_name(None, add_date_suffix_to_file_name=False)

    assert isinstance(log_file_name, Path), "File name is None and no date suffix: the returned file path must be a Path."

    assert log_file_name.stem == TidyLogger.DEFAULT_FILE_NAME, "File name is None and no date suffix: the file stem must be the default file name without the date suffix."

    assert log_file_name.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name is None and no date suffix: the file extension of must be the default extension."

    assert log_file_name.parent == Path("."), "File name is None and no date suffix: the parent directory must be the current directory."

    # File name without extension
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name="test_log")

    assert isinstance(log_file_name, Path), "File name without extension: the returned file path must be a Path."

    assert log_file_name.stem == "test_log_{}".format(date_suffix), "File name without extension: the file stem must contain the date suffix."

    assert log_file_name.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name without extension: the file extension must be the default extension."

    assert log_file_name.parent == Path("."), "File name without extension: the parent directory must be the current directory."

    # File name without extension and no date suffix
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name="test_log", add_date_suffix_to_file_name=False)

    assert isinstance(log_file_name, Path), "File name without extension and no date suffix: the returned file path must be a Path."

    assert log_file_name.stem == "test_log", "File name without extension and no date suffix: the file stem must be the same as specified."

    assert log_file_name.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name without extension and no date suffix: the file extension must be the default extension."

    assert log_file_name.parent == Path("."), "File name without extension and no date suffix: the parent directory must be the current directory."

    # File name with extension
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name="test_log.txt")

    assert isinstance(log_file_name, Path), "File name with extension: the returned file path must be a Path."

    assert log_file_name.stem == "test_log_{}".format(date_suffix), "File name with extension: the file stem must contain the date suffix."

    assert log_file_name.suffix == ".txt", "File name with extension: the file extension must be the same as specified."

    assert log_file_name.parent == Path("."), "File name with extension: the parent directory must be the current directory."

    # File name with extension and no date suffix
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name="test_log.txt", add_date_suffix_to_file_name=False)

    assert isinstance(log_file_name, Path), "File name with extension and no date suffix: the returned file path must be a Path."

    assert log_file_name.stem == "test_log", "File name with extension and no date suffix: the file stem must be the same as specified."

    assert log_file_name.suffix == ".txt", "File name with extension and no date suffix: the file extension must be the same as specified."

    assert log_file_name.parent == Path("."), "File name with extension and no date suffix: the parent directory must be the current directory."

    # File name with parent directory and extension
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name="parent_dir/test_log.txt")

    assert isinstance(log_file_name, Path), "File name with parent directory and extension: the returned file path must be a Path."

    assert log_file_name.stem == "test_log_{}".format(date_suffix), "File name with parent directory and extension: the file stem must be the same as specified."

    assert log_file_name.suffix == ".txt", "File name with parent directory and extension: the file extension must be the same as specified."

    assert log_file_name.parent == Path("parent_dir"), "File name with parent directory and extension: the parent directory must be the same as specified."

    # Environment variable will be used – file name without extension
    log_file_name_env_var_value: str = "env_default_log_name"

    # set environment variable TIDY_LOGGER_DEFAULT_LOG_FILE_NAME
    environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value

    log_file_name: Path = TidyLogger._create_log_file_name()

    assert isinstance(log_file_name, Path), "File name is None, env value is set: the returned file path must be a Path."

    assert log_file_name.stem == "{}_{}".format(
        Path(log_file_name_env_var_value).stem, date_suffix
    ), "File name is None, env value is set: the file stem must contain the date suffix."

    assert log_file_name.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name is None, env value is set: the file extension of must be the default extension."

    assert log_file_name.parent == Path("."), "File name is None, env value is set: the parent directory must be the current directory."

    # remove the environment variable
    environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)

    # Environment variable will be used – file name with extension
    log_file_name_env_var_value: str = "env_default_log_name.txt"

    # set environment variable TIDY_LOGGER_DEFAULT_LOG_FILE_NAME
    environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value

    log_file_name: Path = TidyLogger._create_log_file_name()

    assert isinstance(log_file_name, Path), "File name is None, env value is set: the returned file path must be a Path."

    assert log_file_name.stem == "{}_{}".format(
        Path(log_file_name_env_var_value).stem, date_suffix
    ), "File name is None, env value is set: the file stem must contain the date suffix."

    assert log_file_name.suffix == ".txt", "File name is None, env value is set: the file extension must be the same as specified."

    assert log_file_name.parent == Path("."), "File name is None, env value is set: the parent directory must be the current directory."

    # remove the environment variable
    environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)

    # Invalid characters and reserved names on Windows
    if os.name == "nt":

        # Invalid characters
        file_name_with_invalid_chars: str = "inva|id:log*name?.log"
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name(log_file_name=file_name_with_invalid_chars)

        # Reserved names
        file_name_with_reserved_names: str = "boa/null/aux.log"  # 'null' is not a reserved names on Windows, but 'aux'.
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name(log_file_name=file_name_with_reserved_names, add_date_suffix_to_file_name=False)

        # Environment variable will be used – file name with invalid characters
        log_file_name_env_var_value: str = "inva|id:log*name?.log"
        environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name()
        environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)

        # Environment variable will be used – file name with reserved names
        log_file_name_env_var_value: str = "PRN"
        environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name(add_date_suffix_to_file_name=False)
        environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)

        # Environment variable will be used – file name with reserved names
        log_file_name_env_var_value: str = "boa/nul/aux.log"  # 'nul' and 'aux' is a reserved name on Windows, but 'aux' will get the date suffix!
        environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name()
        environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)

        # Environment variable will be used – file name with reserved names
        log_file_name_env_var_value: str = "boa/null/aux.log"
        environ[TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR] = log_file_name_env_var_value
        with pytest.raises(ValueError):
            TidyLogger._create_log_file_name(add_date_suffix_to_file_name=False)
        environ.pop(TidyLogger.TIDY_LOGGER_LOG_FILE_NAME_ENV_VAR)


def test_log_file_creation():

    # File name is None
    log_file_directory: Path = TidyLogger._create_log_file_directory()
    log_file_name: Path = TidyLogger._create_log_file_name(None)
    log_file_path: Path = log_file_directory / log_file_name
    TidyLogger(log_file_name=None).close()

    assert log_file_path.exists(), "File name is None: the log file has not been created."
    assert log_file_path.is_file(), "File name is None: the log path is not a file."
    remove_log_files_and_empty_directories(log_file_path)

    # A single file name
    log_file_directory: Path = TidyLogger._create_log_file_directory()
    file_name: str = "test_log"
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name=file_name)
    log_file_path: Path = log_file_directory / log_file_name
    TidyLogger(log_file_name=file_name).close()

    assert log_file_path.exists(), "A single name: the log file has not been created."
    assert log_file_path.is_file(), "A single name: the log path is not a file."
    remove_log_files_and_empty_directories(log_file_path)

    # A file name with parent directory
    log_file_directory: Path = TidyLogger._create_log_file_directory()
    file_name: str = "test_dir/test_log"
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name=file_name)
    log_file_path: Path = log_file_directory / log_file_name
    TidyLogger(log_file_name=file_name).close()

    assert log_file_path.exists(), "A file name with parent directory: the log file has not been created."
    assert log_file_path.is_file(), "A file name with parent directory: the log path is not a file."
    remove_log_files_and_empty_directories(log_file_path)

    # A file name with multiple parent directories
    log_file_directory: Path = TidyLogger._create_log_file_directory()
    file_name: str = "parent2/parent1/test_log"
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name=file_name)
    log_file_path: Path = log_file_directory / log_file_name
    TidyLogger(log_file_name=file_name).close()

    assert log_file_path.exists(), "A file name with multiple parent directories: the log file has not been created."
    assert log_file_path.is_file(), "A file name with multiple parent directories: the log path is not a file."
    remove_log_files_and_empty_directories(log_file_path)

    # A file path that is created using app_name and app_author
    log_file_directory: Path = TidyLogger._create_log_file_directory(app_name="AwsomeApp", app_author="GreatAuthor")
    file_name: str = "parent2/parent1/test_log"
    log_file_name: Path = TidyLogger._create_log_file_name(log_file_name=file_name)
    log_file_path: Path = log_file_directory / log_file_name
    TidyLogger(app_name="AwsomeApp", app_author="GreatAuthor", log_file_name=file_name).close()

    assert log_file_path.exists(), "A file name that is created using `app_name` and `app_author`: the log file has not been created."
    assert log_file_path.is_file(), "A file name that is created using `app_name` and `app_author`: the log path is not a file."
    remove_log_files_and_empty_directories(log_file_path)


def remove_log_files_and_empty_directories(file_path: Path) -> None:
    # Remove the log file
    if file_path.is_file():
        file_path.unlink()

    # Remove empty parent directories
    parent_directory: Path = file_path.parent
    while parent_directory != Path(".") or parent_directory != Path.cwd():
        try:
            parent_directory.rmdir()
        except OSError:
            break
        parent_directory = parent_directory.parent
