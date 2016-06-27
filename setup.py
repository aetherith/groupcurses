#!/usr/bin/env python
from os import path
from codecs import open

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='GroupCurses',
    version='0.1.0-alpha',
    description='A terminal interface to the GroupMe platform.',
    long_description=long_description,
    url='https://github.com/aetherith/groupcurses',
    author='Thomas C. Foulds',
    author_email='thomas.foulds@aetherith.net',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='chat GroupMe messaging',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'urwid~=1.3.1',
        'requests~=2.10.0',
        'ruamel.yaml~=0.11.11',
    ],
    entry_points={
        'console_scripts': [
            'gcs=groupcurses:main',
        ]
    },
)
