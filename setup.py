#!/usr/bin/env python
import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ibl_edx_gdpr',
    version='1.0.1',
    description='IBL EDX GDPR API',
    author='IBL',
    author_email='info@ibleducation.com',
    url='https://gitlab.com/iblstudios/ibl-edx-gdpr',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "backoff==1.5.0",
        "smmap>=3.0.5,==4.0.0",
        "validators==0.18.2",
        "yagocd==0.4.4"
    ]
)
