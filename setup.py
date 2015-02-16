#!/usr/bin/env python
import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='console_admin',
    version='0.5',
    description='Theme for Django Admin (Django 1.7)',
    author='Marius Ionescu / Douglas Miranda',
    author_email='marius@mi.www.ro',
    url='https://github.com/mariusionescu/console_admin.git',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='django,admin,skin,theme,bootstrap',
)
