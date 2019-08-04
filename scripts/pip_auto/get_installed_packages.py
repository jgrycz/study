#!/usr/bin/python
from subprocess import check_output

from config import INSTALLED_PACKAGES, PIP


def get_installed_packages():
    pip = PIP if PIP is not None else "pip"
    output = check_output([pip, "list"])
    return " ".join([row.split(" ")[0] for row in output.split('\n')])


if __name__ == "__main__":
    packages = get_installed_packages()
    with open(INSTALLED_PACKAGES, "w") as f:
        f.write(packages)
