# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from setuptools import setup


long_description = open('README.md').read()

setup(name='eventlog_automation',
      version='0.0.1',
      description='Command line script for perform automation of generating release of eventlog',
      long_description=long_description,
      author='Jaroslaw Grycz',
      author_email='jaroslaw.grycz@gmail.com',
      scripts=['eventlog_automation/eventlog_automation_cli.py'])
