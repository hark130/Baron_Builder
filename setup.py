'''
    PURPOSE - The build script for setuptools.  This script tells setuptools about baron_builder.
    NOTE
        https://packaging.python.org/tutorials/packaging-projects/
'''

import setuptools

with open("README.md", "r") as inRM:
    long_desc = inRM.read()
    
setuptools.setup(
    name = "baron_builder",
    version = "0.0.1",
    author = "Joseph Harkleroad",
    author_email = "hark130@gmail.com",
    description = "A save game editor for Owlcat Games' Pathfinder Kingmaker",
    long_description = long_desc,
    long_description_content_type="text/markdown",
    url = "https://github.com/hark130/Baron_Builder",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
        "Intended Audience :: End Users/Desktop",
    ]
)
