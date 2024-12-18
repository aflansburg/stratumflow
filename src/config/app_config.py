"""
This module contains the AppConfig class and any other config related functions
"""

import os
from .logger import get_logger

log = get_logger()


# implementing it as a singleton similar to the
# gang of four's approach but "more Pythonic" ¯\_(ツ)_/¯
# https://python-patterns.guide/gang-of-four/singleton/#a-more-pythonic-implementation
class AppConfig:
    """
    Singleton class for managing the app's configuration.
    """

    _instance = None

    REQUIRED_ENV_VARS = [
        "PAUBOX_EMAIL_API_KEY",
        "PAUBOX_EMAIL_API_URL",
        "PAUBOX_MARKETING_API_KEY",
        "PAUBOX_MARKETING_API_URL",
    ]

    def __new__(cls):
        """
        Create a new instance of the AppConfig class if one does not exist.
        Otherwise, return the existing instance. Singleton FTW

        :param cls: The AppConfig class.

        :return: The AppConfig instance.
        """
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.__load_config(ensure=True)
        return cls._instance

    def __load_config(self, ensure: bool = False) -> None:
        """
        Load the configuration from the environment variables and ensure
        that all required environment variables are set.

        :param self: The AppConfig instance.
        :param ensure: Whether to ensure that required env var are set.
        """

        # explicitly set environment to production in Cloud Run
        self.ENVIRONMENT = os.getenv("ENV") or "dev"

        if self.ENVIRONMENT == "dev":
            log.info(
                "This environment was detected as development. "
                "If this is uneepected, please check the ENV variable."
            )

            from dotenv import load_dotenv

            log.info("Loading .env file.")
            load_dotenv()

        self.ENVIRONMENT = os.getenv("RUN_ENV", "dev")
        self.PAUBOX_EMAIL_API_KEY = os.getenv("PAUBOX_EMAIL_API_KEY")
        self.PAUBOX_EMAIL_API_URL = os.getenv("PAUBOX_EMAIL_API_URL")
        self.PAUBOX_MARKETING_API_KEY = os.getenv("PAUBOX_MARKETING_API_KEY")
        self.PAUBOX_MARKETING_API_URL = os.getenv("PAUBOX_MARKETING_API_URL")

        should_ensure = ensure and os.getenv("ENV") != "test"

        for var in self.REQUIRED_ENV_VARS:
            value = os.getenv(var)
            if value is None and should_ensure:
                raise ValueError(f"{var} must be set")
            setattr(self, var, value)
