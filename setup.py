import os
import re
from setuptools import setup
from setuptools import find_packages


chattiefile = os.path.join(os.path.dirname(__file__),
                           'src', 'chattie', '__init__.py')

# Thanks to SQLAlchemy:
# https://github.com/zzzeek/sqlalchemy/blob/master/setup.py#L104
with open(chattiefile) as stream:
    __version__ = re.compile(
        r".*__version__ = '(.*?)'", re.S
    ).match(stream.read()).group(1)


setup(
    name='chattie',
    description='A framework for making bots in Python. Inspired by Hubot',
    version=__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author="Mathew Robinson",
    author_email="mrobinson@praelatus.io",
    download_url='https://github.com/chasinglogic/Chattie',
    install_requires=[
        'requests',
        'click'
    ],
    extras_require={
        'matrix': ['matrix_client'],
        'telegram': ['telegram']
    },
    entry_points={
        'console_scripts': [
            'chattie = chattie.cli:chattie'
        ],
        'chattie.plugins.tricks': [
            'default_tricks = chattie.tricks',
        ],
        'chattie.plugins.connectors': [
            'telegram = chattie.connectors.telegram',
            'terminal = chattie.connectors.term',
            'matrix = chattie.connectors.matrix'
        ],
        'chattie.plugins.inventories': [
            'json = chattie.inventory.json'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ]
)
