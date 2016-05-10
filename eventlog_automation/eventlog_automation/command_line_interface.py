# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from main_variables import USERNAME, PASSWORD, REPO_NAME, REPO_URL
from debian_dependencies import DebianDependencies
from debian_package import DebianPackageCreator
from github_release import GithubRelease
from logger import get_logger
from functools import wraps
from sys import exit
import argparse
import logging
import os
logger = get_logger()


def check_required_variables(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        if not all([USERNAME, PASSWORD, REPO_NAME, REPO_URL]):
            logger.error("You have to set all variables: USERNAME, PASSWORD,"
                         " REPO_NAME in file main_variables.py")
            exit(-1)
        result = func(*args, **kwargs)
        return result
    return decorate


@check_required_variables
def run_github(args):
    releaser = GithubRelease(USERNAME, PASSWORD, REPO_NAME)
    releaser.create_release(args.tag, args.message)
    logger.info("Release proccess completed!")


@check_required_variables
def run_deb(args):
    if DebianDependencies.check_packages():
        creator = DebianPackageCreator(REPO_URL, REPO_NAME, args.dest)
        creator.create_package()
        logger.info("Creating debian package completed!")


@check_required_variables
def run_docker(args):
    raise NotImplementedError("Docker part is not implemented")


class CommandLineInterface(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description=("Script allow automate github releases,"
                                                            " and produce debian package."),
                                               formatter_class=argparse.RawTextHelpFormatter)
        self._parser.add_argument("-v", "--verbose", help="Print all.", action="store_true")
        subparsers = self._parser.add_subparsers()
        github = subparsers.add_parser("github", help="Create release on github")
        github.add_argument("--message", "-m",
                            default=None,
                            help=("Release message, message longer than one word have to be"
                                  "between apostrophes, <MESSAGE>.")),
        github.add_argument("--tag", "-t",
                            default=None,
                            help="Release tag, (0.1.2).")
        github.set_defaults(func=run_github)

        deb = subparsers.add_parser("deb", help="Create debian package")
        deb.add_argument("--dest", "-d",
                         default=os.getcwd(),
                         type=self._real_path,
                         help="Path to store *.deb file.")
        deb.set_defaults(func=run_deb)

        docker = subparsers.add_parser("docker", help="Create eventlog docker image")
        docker.set_defaults(func=run_docker)

    def __call__(self):
        args = self._parser.parse_args()
        level = "INFO"
        if args.verbose:
            level = "DEBUG"
        logging.basicConfig(level=level, name=REPO_NAME)
        logger.info("Script in {} mode.".format(level))
        args.func(args)

    def _real_path(self, path):
        if not os.path.exists(path):
            error_message = "Path not exist: {} ".format(path)
            logger.error(error_message)
            raise Exception(error_message)
        return path
