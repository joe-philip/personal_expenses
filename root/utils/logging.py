from logging import Filter, LogRecord


class ErrorOnlyFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'ERROR' and record.module != 'crontab'


class WarningOnlyFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'WARNING'


class CronErrorFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'ERROR' and record.module == 'crontab'


class CriticalOnlyFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'CRITICAL'


class InfoOnlyFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelname == 'INFO'
