"""
This setup.py file is an essesntial part of package and distirbuting python project. It is used by setuptools(or distutils in older python version) to define the cindfiguration of your project, such as its metadata, dependencies, and other options.
"""

from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of dependencies.
    """

    requirement_list: List[str] = []

    try:
        with open("requirements.txt", "r") as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore the linee and -e .
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. No dependencies will be installed.")
    return requirement_list


setup(
    name="Network Security",
    version="0.0.1",
    description="A package for network security tools and utilities.",
    author="Suraj Gupta",
    author_email="surajgupta7070031833@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
