import logging
import sys
from src.properties import logging_properties

class LOGGER:

    def getLogger(name):
        logger = logging.getLogger(name)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(logging_properties.logging_template))
        console_handler.setLevel(logging.INFO)

        logger.addHandler(console_handler)
        return logger