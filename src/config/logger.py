import logging
import os
import structlog

_logger = None


def get_logger():
    global _logger
    if _logger is None:
        log_level = logging.NOTSET
        if os.getenv("LOG_LEVEL", "INFO") == "DEBUG":
            log_level = logging.DEBUG

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
                structlog.dev.ConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False,
        )

        _logger = structlog.get_logger()

    return _logger
