"""
setup application
"""
from setuptools import find_packages, setup

# open requirements file
requirements = open('requirements.txt', 'rb')

setup(
    name='feature_requests',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[requirements.read()]
)

# close file
requirements.close()
