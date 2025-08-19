import os
from pathlib import Path

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(settings.BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },

    "formatters": {
        "console_debug": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
        },
        "console_warning": {
            "format": "%(asctime)s [%(levelname)s] %(pathname)s: %(message)s",
        },
        "console_error": {
            "format": "%(asctime)s [%(levelname)s] %(pathname)s: %(message)s",
        },
        "file_general": {
            "format": "%(asctime)s [%(levelname)s] [%(module)s] %(message)s",
        },
        "file_error": {
            "format": "%(asctime)s [%(levelname)s] %(message)s (%(pathname)s)\n%(exc_info)s",
        },
        "file_security": {
            "format": "%(asctime)s [%(levelname)s] [%(module)s] %(message)s",
        },
        "mail_error": {
            "format": "%(asctime)s [%(levelname)s] %(message)s (%(pathname)s)",
        },
    },

    "handlers": {

        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "console_debug",
        },
        "console_warning": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "console_warning",
        },
        "console_error": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "console_error",
        },

        "general_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "general.log"),
            "filters": ["require_debug_false"],
            "formatter": "file_general",
        },

        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "formatter": "file_error",
        },

        "security_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "security.log"),
            "formatter": "file_security",
        },

        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
            "filters": ["require_debug_false"],
            "formatter": "mail_error",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console", "console_warning", "console_error", "general_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["error_file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["error_file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.template": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["security_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
