#-*- coding=utf-8 -*-

import logging

def create_logger():
    logger = logging.getLogger('server')
    logger.setLevel(logging.DEBUG)
    # file handler
    fh = logging.FileHandler('logging.log')
    fh.setLevel(logging.DEBUG)
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger