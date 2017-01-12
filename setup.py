

from setuptools import setup, find_packages


setup(

    name='mdn-graphs',
    version='0.1.0',
    description='MDN graph rendering.',
    url='https://github.com/davidmcclure/mdn-graphs',
    license='MIT',
    author='David McClure',
    author_email='dclure@stanford.edu',
    packages=find_packages(),
    scripts=['bin/mdn'],

)
