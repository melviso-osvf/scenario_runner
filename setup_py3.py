#!/usr/bin/python3

import setuptools

from os import path, system
from setuptools.command.install import install 
from setuptools import setup, find_packages 
from sys import platform

class extra_install(install):
    """Extra operations required for install"""
 	
    user_options = install.user_options + [('reinstall-wxpython', None, 'rebuild and reinstall wxpython')]

    def initialize_options(self):
        super(extra_install, self).initialize_options()

    def run(self):
        "Do extra setup step"
        if platform == "linux" or platform == "linux2":
            # when building inside docker we dont need to be sudo. 
            # otherwise, we must run it as sudoer
            system("apt-get update && apt-get install --no-install-recommends -y python3.6 python3-pip build-essential")
        super(extra_install, self).run()

with open(path.join(path.dirname(__file__),"README.md"), "r") as f:
    long_description = f.read()

with open(path.join(path.dirname(__file__),"requirements.txt"), "r") as f:
    required = f.read().splitlines()

setuptools.setup(
    name='scenario_runner',  
    version='0.9.8',
    author="carla team",
    author_email="carla.simulator@gmail.com",
    description="ScenarioRunner for CARLA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carla-simulator/scenario_runner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.5',
    cmdclass={'install': extra_install},
 )

