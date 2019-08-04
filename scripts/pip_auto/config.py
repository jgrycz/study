from os.path import realpath, split, join


BASE_PATH = realpath(split(__file__)[0])
PYPI = "http://pypi.ute.inside.nsn.com/"
PYPI_PACKAGES = join(BASE_PATH, "pypi_packages")
INSTALLED_PACKAGES = join(BASE_PATH, "installed_packages")
PIP_TEMPLATE = join(BASE_PATH, "pip_template")
PIP_FILE = join(BASE_PATH, "pip")
PIP = "/opt/ute/python/bin/pip"
