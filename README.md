# tidy-logger


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub Release](https://img.shields.io/github/v/release/fa-vahidi/tidy-logger)](https://github.com/fa-vahidi/tidy-logger/releases)
[![GitHub Tag](https://img.shields.io/github/v/tag/fa-vahidi/tidy-logger)](https://github.com/fa-vahidi/tidy-logger/tags)
[![GitHub branch check runs](https://img.shields.io/github/check-runs/fa-vahidi/tidy-logger/main)](https://github.com/fa-vahidi/tidy-logger)
[![PyPI - tidy-logger](https://img.shields.io/pypi/v/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![PyPI - Format](https://img.shields.io/pypi/format/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![PyPI - Status](https://img.shields.io/pypi/status/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tidy-logger)](https://pypi.org/project/tidy-logger/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/tidy-logger)](https://anaconda.org/channels/conda-forge/packages/tidy-logger/overview)
[![Conda Platform](https://img.shields.io/conda/pn/conda-forge/tidy-logger)](https://anaconda.org/channels/conda-forge/packages/tidy-logger/overview)


A repository for a Python logging utility that generates indented log messages with color-coding for different log levels on the console, and also supports logging to files for better tracking and debugging.


> [!NOTE]
> Development for this repository follows the [GitFlow](https://blog.programster.org/git-workflows) workflow.


## Installation

To install the `tidy-logger` package, run the following command:

```bash
pip install tidy-logger
```

## Usage

Here’s an example of how to use the `tidy-logger` utility in a Python project. Start by creating a file named `test_module.py`, as shown below:

```python
import logging
from tidy_logger import TidyLogger

# Initialize the TidyLogger instance
logger = TidyLogger(app_name="AwesomeApp", app_author="GreatAuthor", log_file_name="journal", console_level=logging.DEBUG)

def some_function() -> None:
    # Example log messages
    logger.debug("This is a debug message - Used for debugging during development.")
    logger.info("This is an info message - General application information.")
    logger.warning("This is a warning message - Something might need attention.")
    logger.error("This is an error message - Something went wrong!")
    logger.critical("This is a critical message - Serious error, action required!")

if __name__ == "__main__":
    some_function()

```
Run the newly created module using the following command:

```bash
python -m test_module.py
```

## Console Output

The logs will appear on the console with color-coded log levels, as shown below:

<img src="https://raw.githubusercontent.com/fa-vahidi/tidy-logger/main/assets/tidy_logger_console_output.png" alt="console output" width="672" height="305">

## Options

The environment variable `TIDY_LOGGER_LOG_FILE_DIR` can be set to specify the log file directory if the `log_file_directory` argument is not provided during the initialization of `TidyLogger`. It is recommended to set this environment variable to an absolute path.  

Similarly, the environment variable `TIDY_LOGGER_LOG_FILE_NAME` can be set to set to specify the log file name if the `log_file_name` argument is not provided.  
