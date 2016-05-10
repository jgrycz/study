# -*- coding: utf-8 -*-
"""
:author: Jaroslaw Grycz
:contact: jaroslaw.grycz@gmail.com
"""
from eventlog_automation.command_line_interface import *
import os


class TestCommandLineInterface(object):
    cli = CommandLineInterface()

    def test_github(self):
        args = self.cli._parser.parse_args(["github"])
        assert args.verbose is False
        assert args.tag is None
        assert args.message is None
        assert args.func is run_github

        args = self.cli._parser.parse_args(["github", "-t", "0.2.1",
                                            "--message", "Release 0.2.1"])
        assert args.verbose is False
        assert args.tag is "0.2.1"
        assert args.message is "Release 0.2.1"
        assert args.func is run_github

        args = self.cli._parser.parse_args(["-v", "github", "--tag", "0.2.1",
                                            "-m", "Release 0.2.1"])
        assert args.verbose is True
        assert args.tag is "0.2.1"
        assert args.message is "Release 0.2.1"
        assert args.func is run_github

    def test_deb(self):
        args = self.cli._parser.parse_args(["deb"])
        assert args.verbose is False
        assert args.dest == os.getcwd()
        assert args.func is run_deb

        args = self.cli._parser.parse_args(["deb", "-d", "/tmp/"])
        assert args.verbose is False
        assert args.dest == "/tmp/"
        assert args.func is run_deb

        args = self.cli._parser.parse_args(["deb", "--dest", "/tmp"])
        assert args.verbose is False
        assert args.dest == "/tmp"
        assert args.func is run_deb

    def test_docker(self):
        args = self.cli._parser.parse_args(["--verbose", "docker"])
        assert args.verbose is True
        assert args.func is run_docker
