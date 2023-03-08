from typing import Any

import click
import uvicorn


LOG_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "disco_magnesium": {"level": "INFO"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s  - %(name)s:%(lineno)s - %(message)s"},
    },
}


@click.command()
def disco_magnesium() -> None:
    uvicorn.run(
        "disco_magnesium.api.app:setup_app",
        host="0.0.0.0",
        port=1414,
        reload=True,
        factory=True,
        log_config=LOG_CONFIG
    )


if __name__ == "__main__":
    disco_magnesium()
