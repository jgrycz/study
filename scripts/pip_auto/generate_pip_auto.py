#!/usr/bin/env python
from subprocess import check_output
import re

from get_installed_packages import get_installed_packages
from get_pypi_packages import get_pypi_packages
from config import *


def get_commands():
    output = check_output(["pip", "--help"]).split("\n")
    start, end = 0, 0

    for num, line in enumerate(output):
        if "Commands:" in line:
            start = num
        elif "General Options" in line:
            end = num

    output = output[start + 1:end]
    commands = [line.split()[0] for line in output if line]
    return commands


def get_options(command):
    output = check_output(["pip", command, "--help"])
    opts = set(re.findall(r"(\-\w{1})\,", output))
    opts.update(re.findall(r"(\-\-[\w_-]*)", output))
    return list(opts)


def generate_bash_variable(name, opts):
    return "    {name}=\"{opts}\"\n".format(name=name, opts=" ".join(opts))


def generate_condition(command):
    condition = ("\n    elif [ $command == {command} ] && [[ ${{cur}} == -* ]] ; then\n"
                 "        COMPREPLY=( $(compgen -W \"${{{command}}}\" -- ${{cur}} ) )\n"
                 "        return 0")
    return condition.format(command=command)


def get_file_content(file_path):
    with open(file_path) as f:
        return f.read()


def save(file_path, output):
    with open(file_path, 'w') as f:
        f.write(output)


def main():
    variables = ""
    conditions = ""

    variables += "base_path=\"{}\"\n".format(BASE_PATH)
    commands = get_commands()
    variables += generate_bash_variable("commands", commands)

    for cmd in commands:
        opts = get_options(cmd)
        variables += generate_bash_variable(cmd, opts)
        conditions += generate_condition(cmd)

    template = get_file_content(PIP_TEMPLATE)
    template = template.replace("variables_section", variables)
    template = template.replace("conditions_section", conditions)

    save(PIP_FILE, template)
    save(INSTALLED_PACKAGES, get_installed_packages())
    save(PYPI_PACKAGES, get_pypi_packages(PYPI))

if __name__ == '__main__':
    main()
