#!/usr/bin/env python
import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='ibl_edx_gdpr',
    version='1.0.0',
    description='IBL EDX GDPR API',
    author='IBL',
    author_email='info@ibleducation.com',
    url='https://gitlab.com/iblstudios/ibl-edx-gdpr',
    packages=find_packages(),
    include_package_data=True
)
