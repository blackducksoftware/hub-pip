import os

from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It"s nice, because now 1) we have a top level
# README file and 2) it"s easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hub-pip",
    version="0.0.1",
    author="Black Duck Software",
    author_email="",
    description=(
        "Generates and deploys Black Duck I/O files for use with the Black Duck Hub"),
    license="Apache 2.0",
    keywords="hub-pip blackduck",
    url="https://github.com/blackducksoftware/hub-python-plugin",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=["configparser", "requests", "six", "docopt"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    long_description=read("README.md"),
    classifiers=[],
    entry_points={
        "console_scripts": [
            "hub_pip=hub_pip.Main:cli",
        ],
        "distutils.commands": [
            "hub_pip=hub_pip.BlackDuckPlugin:BlackDuckCommand",
        ]
    },
)
