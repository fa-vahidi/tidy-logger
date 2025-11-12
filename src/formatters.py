import logging


class IndentedMessageFormatter(logging.Formatter):

    default_logging_format: str = "%(asctime)s | %(levelname)s | %(filename)s %(funcName)s() (line: %(lineno)d) [%(name)s]:\n%(message)s"
    default_date_format: str = "%d/%m/%Y %H:%M:%S"

    def __init__(self, fmt: str = None, date_format: str = None, indentation: str = "   "):
        if fmt is None:
            fmt = self.default_logging_format
        if date_format is None:
            date_format = self.default_date_format
        super().__init__(fmt=fmt, datefmt=date_format)
        if indentation is None:
            indentation = ""
        self.indentation = indentation

    def format(self, record: logging.LogRecord) -> str:
        # Format the message with indentation
        if record.msg:
            msg = str(record.getMessage())
            indented_msg = "\n".join(f"{self.indentation}{line}" for line in msg.splitlines())
            indented_msg += "\n" if not indented_msg.endswith("\n") else ""
            record.msg = indented_msg

        return super().format(record)


class ColoredIndentedMessageFormatter(IndentedMessageFormatter):

    def __init__(self, only_apply_on_header: bool = True) -> None:
        super().__init__()
        self.only_apply_on_header = only_apply_on_header

    COLORS = {"DEBUG": "\033[94m", "INFO": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m", "CRITICAL": "\033[95m"}  # Blue  # Green  # Yellow  # Red  # Magenta

    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        if self.only_apply_on_header:
            lines = message.splitlines(True)
            if len(lines) > 0:
                lines[0] = f"{color}{lines[0]}{self.RESET}"
            return "".join(lines)
        else:
            return f"{color}{message}{self.RESET}"
