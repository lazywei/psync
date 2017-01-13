#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'PyYAML>=3.12',
    'watchdog>=0.8.3',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='project-sync',
    version='0.2.0',
    description="A simple tool for synchronizing local project (files) "
                "to remote server.",
    long_description=readme,

    author="Chih-Wei Chang",
    author_email='bert.cwchang@gmail.com',
    url='https://github.com/lazywei/psync',
    packages=[
        'psync',
    ],

    package_dir={'psync':
                 'psync'},

    entry_points={
        'console_scripts': [
            'psync=psync.cli:cli'
        ]
    },

    install_requires=requirements,
    license="MIT license",

    zip_safe=False,

    keywords='project sync rsync auto watch',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    test_suite='tests',
    tests_require=test_requirements,
)
