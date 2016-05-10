# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from logger import get_logger
from github import Github
logger = get_logger()


class GithubRelease(object):
    def __init__(self, username, password, repo_name):
        self._username = username
        self._password = password
        self._repo_name = repo_name

    def create_release(self, tag=None, message=None):
        githubuser = GithubUser(self._username, self._password)
        githubuser.authenticate()
        githubrepo = GithubRepo(githubuser.get_user_repo(self._repo_name))
        githubrepo.create_release(tag, message)


class GithubUser(object):
    _user = None

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def authenticate(self):
        logger.info("User authentication.")
        try:
            github = Github(self._username, self._password)
            self._user = github.get_user()
        except Exception as e:
            raise Exception("Can not authenticate user {}.\n{}".format(self._username, str(e)))

    def get_user_repo(self, name):
        logger.info("Geting repository: {}.".format(name))
        try:
            repo = self._user.get_repo(name)
            return repo
        except Exception as e:
            raise Exception("Problem with geting repository: {}\n{}".format(name, str(e)))


class GithubRepo(object):
    def __init__(self, repo):
        self._repo = repo

    @property
    def name(self):
        return self._repo.name

    def _get_tags(self):
        try:
            tags = self._repo.get_tags()
            return tags
        except Exception as e:
            raise Exception("Problem with geting tags from: {}\n{}".format(self.name, str(e)))

    def generate_next_tag(self):
        logger.info("Generating new tag.")
        tag = [tag.name for tag in self._get_tags()][0]
        next_num = int(tag[-1]) + 1
        tag = tag[:-1] + str(next_num)
        return tag

    def generate_message(self):
        logger.info("Generating release message.")
        message = ("Changelog:\n"
                   "003ec9f (HEAD -> master, origin/master, origin/HEAD) Renamed test exampl file\n"
                   "05c20a3 Corected test example\n"
                   "afe6d88 Created required files to build and install package\n"
                   "ed7027d Added templates\n"
                   "2d80977 created dirs and needed files\n"
                   "8e6ba72 Create README.md\n"
                   "7c9ffdc Initial commit\n")
        return message

    def create_release(self, tag, message):
        logger.info("Releasing repository: {}.".format(self.name))
        if tag is None:
            tag = self.generate_next_tag()
        if message is None:
            message = self.generate_message()

        self._repo.create_git_release(tag, "Release: {}".format(tag), message)
