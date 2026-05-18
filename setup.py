from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines, comments, and local package installs (-e .)
                if requirement and not requirement.startswith('#') and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    return requirement_list

setup(
    name="networksecurity",
    version="0.0.1",
    author="Suraj Gupta",
    author_email="surajgupta7070031833@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
