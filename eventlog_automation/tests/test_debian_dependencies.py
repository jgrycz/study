# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from eventlog_automation.debian_dependencies import DebianDependencies
from mock import MagicMock, patch


class TestDebianDependencies(object):
    @patch('subprocess.Popen')
    def test_fail_check_package(self, mock_popen):
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ("", ""), 'returncode': 1}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        result = DebianDependencies._check_package("package")
        assert result is False

    @patch('subprocess.Popen')
    def test_pass_check_package(self, mock_popen):
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ("", ""), 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        result = DebianDependencies._check_package("package")
        assert result is True

    def test_fail_create_message_and_get_status(self):
        status, message = DebianDependencies._create_message_and_get_status(["package"])
        assert status is False
        assert message == ("Not installed packages:\n\t\t"
                           "package"
                           "\nTry use command:\nsudo apt-get install " + "package")

    def test_pass_create_message_and_get_status(self):
        status, message = DebianDependencies._create_message_and_get_status([])
        assert status is True
        assert message == "All required packages are installed"

    def test_pass_check_packages(self):
        DebianDependencies._check_package = MagicMock(return_value=True)
        status = DebianDependencies.check_packages()
        assert status is True

    def test_fail_check_packages(self):
        DebianDependencies._check_package = MagicMock(return_value=False)
        status = DebianDependencies.check_packages()
        assert status is False
