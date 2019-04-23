import sys
from setuptools import setup, find_packages

py_version = sys.version_info[:2]

if py_version < (3, 0):
    raise RuntimeError('Git-php-lint requires Python version > 3')

setup(
    name="git-php-lint",
    packages=find_packages(),
    url="https://www.webdal.ro",
    version="1.0.0",
    description="Lint the PHP added in git project",
    author="Dumitru Alexandru",
    license="MIT",
    package_data={
        'gitphplint': ['HELP.rst']
    },
    entry_points={
        "console_scripts": [
            "git-php-lint = gitphplint.__main__:main",
        ],
    }
)
