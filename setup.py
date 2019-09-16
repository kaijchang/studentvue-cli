from setuptools import setup

setup(
    name='studentvue-cli',
    entry_points={
        'console_scripts': ['studentvue=cli.main:main'],
    }
)
