# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="copenhagen-apartment-finder",
    version="0.1.0",
    description="Scrape DBA and Boliga to find newly-listed apartments in Copenhagen",
    license="MIT",
    author="Andrew Keating",
    packages=find_packages(),
    install_requires=[
        'BeautifulSoup==3.2.1',
        'Requests==2.9.1'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
