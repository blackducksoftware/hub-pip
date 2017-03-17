import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hub_python_plugin",
    version = "0.0.1",
    author = "Black Duck Software",
    author_email = "",
    description = ("Generates and deploy's Black Duck I/O files for use with the Black Duck Hub"),
    license = "Apache 2.0",
    keywords = "hub_python_plugin blackduck",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=[],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache 2.0 License",
    ]
)
