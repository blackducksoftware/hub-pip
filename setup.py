import os

from setuptools import setup, find_packages

package_name = "hub-pip"
package_version = "1.0.0"

setup(
    name=package_name,
    version=package_version,
    author="Black Duck Software",
    author_email="bdsoss@blackducksoftware.com",
    description=(
        "Generates and deploys Black Duck I/O files for use with the Black Duck Hub"),
    license="Apache 2.0",
    keywords="hub-pip blackduck",
    url="https://github.com/blackducksoftware/hub-pip",
    install_requires=["configparser", "requests", "six", "docopt"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['*.md', '*.ini'],
    },
    entry_points={
        "console_scripts": [
            "hub_pip=hub_pip.Main:cli",
        ],
        "distutils.commands": [
            "hub_pip=hub_pip.BlackDuckPlugin:BlackDuckCommand",
        ]
    },
)
