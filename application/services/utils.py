import random
import string
import logging
from logging.handlers import RotatingFileHandler


def generate_random_code(size=8):
    """
    Generate random code with length size

    generates random characters with length matching the given
    input parameter, size. if no size is specified, the random
    code length is set as 8.

    :param size:
    :return:
    """

    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.punctuation) for _ in range(size))


def create_log_file(log_name, log_level='INFO'):
    """
    creates a rotating log file

    creates a rotating log file with default
    log level set as 'INFO'. creates a new file
    when current log file reaches 15kb and
    creates 2 backup files.
    :param log_name:
    :param log_level:
    :return:
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # add a rotating file handler
    handler = RotatingFileHandler(log_name, maxBytes=15000, backupCount=2)
    logger.addHandler(handler)

    return logger

