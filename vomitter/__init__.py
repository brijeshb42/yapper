"""Create some default loggers."""
import sys
from os.path import join, dirname, abspath
import logging
from logging.handlers import RotatingFileHandler

from .logger import BaseLogger, GmailSMTPHandler
from config import Config


ALGO = "algo"
FORMAT_LOG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FORMAT_TIME = "%d-%m-%Y %H:%M:%S"
MAX_LOG_FILE_SIZE = 1024*1024*2
DEF_LEVEL = logging.DEBUG


def get_formatter():
    """Return a default formatter."""
    return logging.Formatter(FORMAT_LOG, FORMAT_TIME)


def get_mail_formatter():
    """Default mail formatter."""
    return logging.Formatter("""
Message type :       %(levelname)s
Location :           %(pathname)s:%(lineno)d
Module :             %(module)s
Function :           %(funcName)s
Time :               %(asctime)s

Message :

%(message)s
""", FORMAT_TIME)


def get_console_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(get_formatter())
    return handler


def get_file_handler():
    """Return a RotatingFileHandler."""
    """To be used by various loggers across the app."""
    log_file_name = join(
        join(dirname(dirname(abspath(__file__))), "logs"), "logfile.log")
    handler = RotatingFileHandler(
        log_file_name, maxBytes=MAX_LOG_FILE_SIZE, backupCount=50)
    handler.setLevel(DEF_LEVEL)
    return handler


def get_console_vomitter(name="app", level=DEF_LEVEL):
    """Return a console logger."""
    logger = BaseLogger(name, level)
    handler = get_console_handler()
    logger.addHandler(handler)
    return logger


def get_file_vomitter(name="app", level=DEF_LEVEL):
    """Return a console logger."""
    logger = get_console_vomitter(name, level)
    handler = get_file_handler()
    handler.setFormatter(get_formatter())
    logger.addHandler(handler)
    return logger


def get_mail_handler(name="app", level=DEF_LEVEL):
    """Mail handler."""
    handler = GmailSMTPHandler(
        (Config.MAIL_HOST, Config.MAIL_PORT),
        Config.MAIL_FROM,
        Config.MAIL_TO,
        "%s Server Error." % Config.APP_NAME,
        (Config.MAIL_FROM, Config.MAIL_PASSWORD))
    handler.setLevel(level)
    handler.setFormatter(get_mail_formatter())
    return handler


def get_mail_vomitter(name="app", level=DEF_LEVEL):
    """Return a mail logger."""
    logger = get_file_vomitter(name, level)
    logger.addHandler(get_mail_handler(name, level))
    return logger

LOGGER = get_console_vomitter(name="Yapper", level=logging.DEBUG)
PROD_LOGGER = get_mail_vomitter(name="Mailer", level=logging.ERROR)
# PROD_LOGGER = get_file_vomitter(name="Yapper", level=logging.ERROR)
