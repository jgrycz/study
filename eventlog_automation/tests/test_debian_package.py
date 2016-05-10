# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
import eventlog_automation.debian_package as deb
import pytest
from mock import MagicMock, patch


class TestDebianPackage(object):
    def test_prepare_workspace(self):
        deb.time.ctime = MagicMock(return_value='Sun Mar 27 10:31:55 2016')
        deb.os.mkdir = MagicMock()
        creator = deb.DebianPackageCreator("", "", "")
        creator._prepare_workspace()
        assert creator.workspace_path == "/tmp/eventlog_workspace10_31_55"

    def test_clean_workspace(self):
        def mock_execute_cmd_and_check_result(cmd):
            assert cmd == ["sudo", "rm", "-rf", "/tmp/eventlog_workspace10_31_55"]

        creator = deb.DebianPackageCreator("", "", "")
        creator.workspace_path = "/tmp/eventlog_workspace10_31_55"
        creator.repo_path = "/tmp/eventlog_workspace10_31_55/eventlog"
        creator._execute_cmd_and_check_result = mock_execute_cmd_and_check_result
        creator._clean_workspace()

    def test_archive_debian_package(self):
        def mock_move(src, dest):
            assert src == "/tmp/eventlog_workspace10_31_55/eventlog/a.deb"

        deb.os.listdir = MagicMock(return_value=["a", "b", "a.deb", "b.deby"])
        deb.shutil.move = mock_move
        creator = deb.DebianPackageCreator("", "eventlog", "")
        creator.workspace_path = "/tmp/eventlog_workspace10_31_55"
        creator.repo_path = "/tmp/eventlog_workspace10_31_55/eventlog"
        creator._archive_debian_package()

    @patch('subprocess.Popen')
    def test_pass_execute_cmd_and_check_result(self, mock_subproc_popen):
        process_mock = MagicMock()
        attrs = {'wait.return_value': None, 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock
        creator = deb.DebianPackageCreator("", "", "")
        creator.workspace_path = "/tmp/eventlog_workspace10_31_55"
        creator._execute_cmd_and_check_result(["a", "b", "c"])
        assert mock_subproc_popen.called is True

    @patch('subprocess.Popen')
    def test_fail_execute_cmd_and_check_result(self, mock_popen):
        process_mock = MagicMock()
        attrs = {'wait.return_value': None, 'returncode': 1}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        creator = deb.DebianPackageCreator("", "", "")
        creator.workspace_path = "/tmp/eventlog_workspace10_31_55/eventlog"
        with pytest.raises(Exception):
            creator._execute_cmd_and_check_result(["a", "b", "c"])

    def test_create_deb(self):
        def mock_execute_cmd_and_check_result(self, cmd):
            self.cmds.append(cmd)

        deb.DebianPackageCreator._execute_cmd_and_check_result = mock_execute_cmd_and_check_result
        creator = deb.DebianPackageCreator("", "eventlog", "")
        creator._get_version = lambda: "0.1.2"
        creator.cmds = []
        creator._create_deb()
        expected_result = [['./autogen.sh'], ['./configure'], ['make'],
                           ['sudo', 'checkinstall', '--pkgversion', '0.1.2', '-y'],
                           ['sudo', 'dpkg', '-r', 'eventlog']]
        assert expected_result == creator.cmds
