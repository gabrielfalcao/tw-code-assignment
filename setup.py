# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# https://setuptools.readthedocs.io/en/latest/setuptools.html#adding-setup-arguments
setup(
    name='tw-conference-track-manager',
    version='0.0.1',
    description="\n".join([
        'Manage a tech conference'
    ]),
    entry_points={
        'console_scripts': [
            'tw-conf-parse = tw_conference_manager.cli:main',
        ],
    },
    author=u"Gabriel Falcao",
    author_email='gabriel@nacaolivre.org',
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    package_data={
        'tw_conference_manager': '*.rst *.txt docs/source/* docs/*'.split(),
    },
    zip_safe=False,
)
