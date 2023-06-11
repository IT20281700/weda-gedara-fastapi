import logging
import os
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO")
)


def getLogger(module_name: str):
    return logging.getLogger(module_name.upper())
