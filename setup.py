#!/usr/bin/env python
import os
from setuptools import find_packages, setup
from glob import glob
from os.path import basename, splitext

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from openedx.core.release import RELEASE_LINE

# Simple patch for Ironwood/KOA
apps = []
if RELEASE_LINE == 'ironwood':
    apps = ['smmap==3.0.5', "validators==0.17"]

elif RELEASE_LINE == 'koa':
    apps = ['smmap==4.0.0',"validators==0.18.2",]
else:
    pass


setup(
    name='ibl_edx_gdpr',
    version='1.3.4',
    description='IBL EDX GDPR API',
    author='IBL',
    author_email='info@ibleducation.com',
    url='https://gitlab.com/iblstudios/ibl-edx-gdpr',
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=[
        "backoff==1.5.0",
        "yagocd==0.4.4"
    ],
    entry_points={
        'lms.djangoapp': [
            'ibl_edx_gdpr = ibl_edx_gdpr.apps:EdxGDPRConfig'
        ],
        'cms.djangoapp': [
            'ibl_edx_gdpr = ibl_edx_gdpr.apps:EdxGDPRConfig'
        ]
    },
)
