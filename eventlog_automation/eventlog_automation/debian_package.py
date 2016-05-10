# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from logger import get_logger
from functools import wraps
from git import Git
import subprocess
import time
import os
import shutil
logger = get_logger()


def return_to_cwd(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        cwd = os.getcwd()
        result = func(*args, **kwargs)
        os.chdir(cwd)
        return result
    return decorate


def clone_repo(repo_url, repo_dest_path):
    logger.info("Cloning repository: {}, into {}".format(repo_url, repo_dest_path))
    Git().clone(repo_url, repo_dest_path)


class DebianPackageCreator(object):
    def __init__(self, url, repo_name, dest_path):
        self.workspace_path = None
        self.repo_path = None
        self.url = url
        self.dest_path = dest_path
        self.repo_name = repo_name

    def _prepare_workspace(self):
        logger.info("Preparing workspace.")
        workspace_name = "eventlog_workspace" + time.ctime()[11:-5].replace(":", "_")
        self.workspace_path = os.path.join("/tmp", workspace_name)
        self.repo_path = os.path.join(self.workspace_path, self.repo_name)
        os.mkdir(self.workspace_path)

    def _clean_workspace(self):
        logger.info("Cleaning workspace.")
        logger.debug(self.workspace_path)
        self._execute_cmd_and_check_result(["sudo", "rm", "-rf", self.workspace_path])

    def _archive_debian_package(self):
        deb_name, = [f for f in os.listdir(self.repo_path) if f.endswith(".deb")]
        logger.info("Moving {} to {}.".format(deb_name, self.dest_path))
        shutil.move(os.path.join(self.repo_path, deb_name), self.dest_path)

    def _execute_cmd_and_check_result(self, cmd):
        logger.info("Executing command: {}".format(" ".join(cmd)))
        proc = subprocess.Popen(cmd)
        proc.wait()
        if proc.returncode != 0:
            error_message = "Executed command failed: {}".format(" ".join(cmd))
            logger.error(error_message)
            raise Exception(error_message)

    def _get_version(self):
        with open(os.path.join(self.repo_path, "VERSION")) as f:
            version = f.read()
            return version[:-1]

    def _create_deb(self):
        self._execute_cmd_and_check_result(["./autogen.sh"])
        self._execute_cmd_and_check_result(["./configure"])
        self._execute_cmd_and_check_result(["make"])
        version = self._get_version()
        self._execute_cmd_and_check_result(["sudo", "checkinstall", "--pkgversion", version, "-y"])
        self._execute_cmd_and_check_result(["sudo", "dpkg", "-r", self.repo_name])

    @return_to_cwd
    def create_package(self):
        try:
            self._prepare_workspace()
            clone_repo(self.url, self.repo_path)
            os.chdir(os.path.join(self.repo_path))
            self._create_deb()
            self._archive_debian_package()
        finally:
            self._clean_workspace()
