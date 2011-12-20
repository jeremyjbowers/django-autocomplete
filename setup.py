#!/usr/bin/env python
from distutils.core import setup

setup(name='autocomplete',
        version='0.2',
        description='The Washington Post\'s app for creating admin foreign key autocompletion fields.',
        author='Jeremy Bowers',
        author_email='jeremyjbowers@gmail.com',
        url='https://github.com/jeremyjbowers/django-autocomplete',
        packages = ['autocomplete',],
        license = 'MIT',
        package_data = {'': [
            'media/autocomplete/js/*.js',
            'media/autocomplete/css/*.css',
            'templates/admin/autocomplete/*.html',
        ]},
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
)