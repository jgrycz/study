# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from eventlog_automation.logger import get_logger
import subprocess
logger = get_logger()


class DebianDependencies(object):
    dependencies = ["build-essential", "automake", "autoconf", "libtool",
                    "pkg-config", "libcurl4-openssl-dev", "intltool",
                    "libxml2-dev", "libgtk2.0-dev", "libnotify-dev",
                    "libglib2.0-dev", "libevent-dev", "checkinstall"]

    @staticmethod
    def _check_package(package):
        proc = subprocess.Popen(["dpkg-query", "-l", package], stdout=subprocess.PIPE)
        out = proc.communicate()
        logger.debug(out[0])
        status = True
        if proc.returncode != 0:
            status = False
        return status

    @staticmethod
    def _create_message_and_get_status(packages):
        status = True
        message = "All required packages are installed"
        if packages:
            status = False
            message = "Not installed packages:\n\t\t"
            message += "\n\t\t".join(packages)
            message += "\nTry use command:\nsudo apt-get install " + " ".join(packages)
        return status, message

    @staticmethod
    def check_packages():
        debian = DebianDependencies
        installed = [debian._check_package(package) for package in debian.dependencies]
        to_install = [k for k, v in zip(debian.dependencies, installed) if not v]
        status, message = debian._create_message_and_get_status(to_install)
        logger.info(message)
        return status
