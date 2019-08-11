from setuptools import setup

setup(
    name='pygfs',
    version='0.1.0',
    packages=[''],
    package_dir={'': 'pygfs'},
    url='https://github.com/havocesp/pygfs',
    license='UNLICENSE',
    author='Daniel J. Umpierrez',
    author_email='umpierrez@pm.me',
    description='Python Google Flights Scrapper',
    requirements=['dateparser', 'lxml', 'splinter']
)
