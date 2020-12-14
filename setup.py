import setuptools
from os import system,getenv,path,mkdir,listdir

with open("README.md","r") as fh:
    long_description = fh.read()

with open("requirements.txt") as require:
    install_requires = require.readlines()

setuptools.setup(
        name = "twittercli",
        version = "0.0.1",
        author = "Stiven Roytman",
        author_email = "stiven.roytman@wayne.edu",
        description = "A Selenium-based twitter interface for python and command line that I am writing for shits and giggles.",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/stivenroytman/twitter-cli",
        packages = setuptools.find_packages(),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GPLv3",
            "Operating System :: Linux",
        ],
        python_requires='>=3.8',
        install_requires = install_requires,
)
        

