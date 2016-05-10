# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from main_variables import REPO_NAME
import logging


def get_logger():
    return logging.getLogger(REPO_NAME)
