#!/usr/bin/env python

from setuptools import setup, find_packages

DESCRIPTION = 'Simple and unrestrictive staticfile preprocessor for Django.'

setup(
    name='django-transformfiles',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Jeremy Swinarton',
    author_email='jeremy@swinarton.com',
    url='https://github.com/jswinarton/django-transformfiles',
    licence='Public Domain',
    packages=find_packages(),
    package_data={
        'transformfiles': ['management/commands/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
