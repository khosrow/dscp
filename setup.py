# from distutils.core import setup
from setuptools import setup

import dscp

setup(
    name='dscp',
    version=dscp.__version__,
    author=dscp.__author__,
    author_email='khosrow.ebrahimpour@ssc-spc.gc.ca',
    packages=['dscp'],
    url='http://github.com/khosrow/dscp',
    license='LICENSE',
    description=dscp.__doc__.rstrip(),
    entry_points={
        'console_scripts': [
            'dscp = dscp.dscp:main',
        ],
    },
)
