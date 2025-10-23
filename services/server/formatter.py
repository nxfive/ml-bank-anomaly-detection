from pythonjsonlogger import jsonlogger


class CleanUvicornFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        if hasattr(record, "color_message"):
            delattr(record, "color_message")
        return super().format(record)
