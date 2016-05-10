# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
import eventlog_automation.github_release as release
import pytest

from mock import MagicMock


class MockUser(object):
    pass


class TestGithubUser(object):
    def test_fail_get_user_repo(self):
        user = release.GithubUser("nonexisting", "user")
        user._user = MockUser()
        user._user.get_repo = MagicMock(side_effect=Exception())
        with pytest.raises(Exception):
            user.get_user_repo("name")

    def test_pass_get_user_repo(self):
        user = release.GithubUser("nonexisting", "user")
        user._user = MockUser()
        expected_value = "name"
        user._user.get_repo = MagicMock(return_value=expected_value)
        assert expected_value == user.get_user_repo("name")

    def test_fail_authenticate_user(self):
        release.Github = MagicMock(side_effect=Exception())
        user = release.GithubUser("nonexisting", "user")
        with pytest.raises(Exception):
            user.authenticate()


class MockRepo(object):
    pass


class MockTag(object):
    def __init__(self, name):
        self.name = name


class TestGithubRepo(object):
    def test_name(self):
        repo = release.GithubRepo(MockRepo())
        repo._repo.name = "eventlog"
        assert repo.name == "eventlog"

    def test_fail_get_tags(self):
        repo = release.GithubRepo(MockRepo())
        repo._repo.get_tags = MagicMock(side_effect=Exception())
        with pytest.raises(Exception):
            repo._get_tags()

    def test_pass_get_tags(self):
        repo = release.GithubRepo(MockRepo())
        expected_value = [u'0.0.1']
        repo._repo.get_tags = MagicMock(return_value=expected_value)
        assert expected_value == repo._get_tags()

    def test_generate_next_tag(self):
        repo = release.GithubRepo(MockRepo())
        repo._repo.get_tags = MagicMock(return_value=[MockTag(u'0.0.1')])
        expected_value = '0.0.2'
        assert expected_value == repo.generate_next_tag()

        repo._repo.get_tags = MagicMock(return_value=[MockTag(u'0.0.2'), MockTag(u'0.0.1')])
        expected_value = '0.0.3'
        assert expected_value == repo.generate_next_tag()

        repo._repo.get_tags = MagicMock(return_value=[MockTag(u'0.0.9'), MockTag(u'0.0.1')])
        expected_value = '0.0.10'
        assert expected_value == repo.generate_next_tag()

        repo._repo.get_tags = MagicMock(return_value=[MockTag(u'0.0.10'), MockTag(u'0.0.1')])
        expected_value = '0.0.11'
        assert expected_value == repo.generate_next_tag()
