import logging
import os
logging.basicConfig(level=logging.DEBUG, filename="py_log.log",
                    filemode="w", format="[%(levelname)s] --> %(message)s")

def debug(msg):
    logging.debug(msg)

def info(msg):
    logging.info(msg)

def warn(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)

def critical(msg):
    logging.critical(msg)

if __name__ == "__main__":
    logging.info("I AM")