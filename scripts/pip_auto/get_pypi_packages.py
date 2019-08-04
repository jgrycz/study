#!/usr/bin/python
from urllib import urlopen
import re

from config import PYPI, PYPI_PACKAGES


def get_pypi_packages(pypi):
    html = urlopen(pypi).read().replace("_", "-")
    results = re.findall(r'<a href\=\"(.*)/\"', html)[1:]
    return " ".join(results)


if __name__ == '__main__':
    packages = get_pypi_packages(PYPI)
    with open(PYPI_PACKAGES, "w") as f:
        f.write(packages)
