# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='granite',
    version='0.1.0',
    description='A benchmark support library',
    long_description=readme,
    author='Julien BERNARD',
    author_email='raplonu.jb@gmail.com',
    url='https://github.com/raplonu/granite',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)