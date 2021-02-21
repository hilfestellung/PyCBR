import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="PyCBR",
    version="1.0.0",
    description="Library for projects to use with Case Based Reasoning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hilfestellung/PyCBR",
    author="Christian Dein",
    author_email="office@realpython.com",
    license="LGPL-2.1-or-later",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["cbrlib"],
    include_package_data=True,
    install_requires=["PyYAML"],
)