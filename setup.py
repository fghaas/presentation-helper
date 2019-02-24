#!/usr/bin/env python

import os

from setuptools import setup

DIR = os.path.dirname(os.path.realpath(__file__))
README = os.path.join(DIR, 'README.rst')


with open(README) as readme:
    setup(
        name='presentation-helper',
        use_scm_version=True,
        description='presentation-helper: '
                    'Creates a presentation skeleton '
                    'from a simple YAML configuration',
        long_description=readme.read(),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Multimedia :: Graphics :: Presentation',
            'Topic :: Text Processing :: Markup',
        ],
        url='https://github.com/fghaas/presentation-helper',
        author='Florian Haas',
        author_email='xahteiwi@gmail.com',
        license='GPLv3',
        packages=[
            'presentationhelper',
        ],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'presentation-helper=presentationhelper.cli:main',
            ],
        },
        install_requires=[
            'Jinja2>=2.9',
            'PyYAML>=4.2b1'
        ],
        setup_requires=['setuptools-scm'],
    )
