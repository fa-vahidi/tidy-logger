import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tidy_logger import TidyLogger  # noqa: E402


def test_create_file_path():

    date_suffix: str = datetime.now().strftime("%Y%m%d")

    # File name is None
    file_path = TidyLogger._create_file_path(None)

    assert isinstance(file_path, Path), "File name is None: the returned file path must be a Path object."

    assert file_path.stem[: len(TidyLogger.DEFAULT_FILE_NAME)] == TidyLogger.DEFAULT_FILE_NAME, "File name is None: the file stem must be the default file name."

    assert file_path.stem == "{}_{}".format(TidyLogger.DEFAULT_FILE_NAME, date_suffix), "File name is None: the file stem must contain the date suffix."

    assert file_path.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name is None: the file extension of must be the default extension."

    assert file_path.parent == Path("."), "File name is None: the parent directory must be the current directory."

    # File name is None and no date suffix
    file_path = TidyLogger._create_file_path(None, add_date_suffix_to_file_name=False)

    assert isinstance(file_path, Path), "File name is None and no date suffix: the returned file path must be a Path object."

    assert file_path.stem == TidyLogger.DEFAULT_FILE_NAME, "File name is None and no date suffix: the file stem must be the default file name without the date suffix."

    assert file_path.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name is None and no date suffix: the file extension of must be the default extension."

    assert file_path.parent == Path("."), "File name is None and no date suffix: the parent directory must be the current directory."

    # File name without extension
    file_path = TidyLogger._create_file_path("test_log")

    assert isinstance(file_path, Path), "File name without extension: the returned file path must be a Path object."

    assert file_path.stem == "test_log_{}".format(date_suffix), "File name without extension: the file stem must contain the date suffix."

    assert file_path.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name without extension: the file extension must be the default extension."

    assert file_path.parent == Path("."), "File name without extension: the parent directory must be the current directory."

    # File name without extension and no date suffix
    file_path = TidyLogger._create_file_path("test_log", add_date_suffix_to_file_name=False)

    assert isinstance(file_path, Path), "File name without extension and no date suffix: the returned file path must be a Path object."

    assert file_path.stem == "test_log", "File name without extension and no date suffix: the file stem must be the same as specified."

    assert file_path.suffix == TidyLogger.DEFAULT_FILE_EXTENSION, "File name without extension and no date suffix: the file extension must be the default extension."

    assert file_path.parent == Path("."), "File name without extension and no date suffix: the parent directory must be the current directory."

    # File name with extension
    file_path = TidyLogger._create_file_path("test_log.txt")

    assert isinstance(file_path, Path), "File name with extension: the returned file path must be a Path object."

    assert file_path.stem == "test_log_{}".format(date_suffix), "File name with extension: the file stem must contain the date suffix."

    assert file_path.suffix == ".txt", "File name with extension: the file extension must be the same as specified."

    assert file_path.parent == Path("."), "File name with extension: the parent directory must be the current directory."

    # File name with extension and no date suffix
    file_path = TidyLogger._create_file_path("test_log.txt", add_date_suffix_to_file_name=False)

    assert isinstance(file_path, Path), "File name with extension and no date suffix: the returned file path must be a Path object."

    assert file_path.stem == "test_log", "File name with extension and no date suffix: the file stem must be the same as specified."

    assert file_path.suffix == ".txt", "File name with extension and no date suffix: the file extension must be the same as specified."

    assert file_path.parent == Path("."), "File name with extension and no date suffix: the parent directory must be the current directory."

    # File name with parent directory and extension
    file_path = TidyLogger._create_file_path("parent_dir/test_log.txt")

    assert isinstance(file_path, Path), "File name with parent directory and extension: the returned file path must be a Path object."

    assert file_path.stem == "test_log_{}".format(date_suffix), "File name with parent directory and extension: the file stem must be the same as specified."

    assert file_path.suffix == ".txt", "File name with parent directory and extension: the file extension must be the same as specified."

    assert file_path.parent == Path("parent_dir"), "File name with parent directory and extension: the parent directory must be the same as specified."

    # Invalid characters and reserved names on Windows
    if os.name == "nt":

        # Invalid characters
        file_name_with_invalid_chars: str = "inva|id:log*name?.log"
        with pytest.raises(ValueError):
            TidyLogger._create_file_path(file_name_with_invalid_chars)

        # Reserved names
        file_name_with_reserved_names: str = "boa/null/aux.log"
        with pytest.raises(ValueError):
            TidyLogger._create_file_path(file_name_with_reserved_names)


def test_log_file_creation():

    # File name is None
    file_path: Path = TidyLogger._create_file_path(None)
    TidyLogger(file_name=None).close()

    assert file_path.is_file(), "File name is None: the log path is not a file."
    assert file_path.exists(), "File name is None: the log file has not been created."
    remove_log_files_and_empty_directories(file_path)

    # A single file name
    file_name: str = "test_log"
    file_path: Path = TidyLogger._create_file_path(file_name)
    TidyLogger(file_name=file_name).close()

    assert file_path.is_file(), "A single name: the log path is not a file."
    assert file_path.exists(), "A single name: the log file has not been created."
    remove_log_files_and_empty_directories(file_path)

    # A file name with parent directory
    file_name: str = "test_dir/test_log"
    file_path: Path = TidyLogger._create_file_path(file_name)
    TidyLogger(file_name=file_name).close()

    assert file_path.is_file(), "A file name with parent directory: the log path is not a file."
    assert file_path.exists(), "A file name with parent directory: the log file has not been created."
    remove_log_files_and_empty_directories(file_path)

    # A file name with multiple parent directories
    file_name: str = "parent2/parent1/test_log"
    file_path: Path = TidyLogger._create_file_path(file_name)
    TidyLogger(file_name=file_name).close()

    assert file_path.is_file(), "A file name with multiple parent directories: the log path is not a file."
    assert file_path.exists(), "A file name with multiple parent directories: the log file has not been created."
    remove_log_files_and_empty_directories(file_path)


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
