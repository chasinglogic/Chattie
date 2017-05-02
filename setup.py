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


# Thanks to Pagure:
# https://pagure.io/pagure/blog/master/f/setup.py
def get_requirements(requirements_file='requirements.txt'):
    """
    Get the contents of a file listing the requirements.

    Returns:
        the list of requirements, or an empty list if
        `requirements_file` could not be opened or read
    :return type: list
    """
    with open(requirements_file) as f:
        return [
            line.rstrip().split('#')[0]
            for line in f.readlines()
            if not line.startswith('#')
        ]


setup(
    name='chattie',
    description='A framework for making bots in Python. Inspired by Hubot',
    version=__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author="""
Mathew Robinson <mrobinson@praelatus.io>
    """,
    download_url='https://github.com/chasinglogic/Chattie/releases',
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'chattie = chattie.cli:chattie'
        ],
        'chattie.plugins.tricks': [
            'default_tricks = chattie.tricks',
        ],
        'chattie.plugins.connectors': [
            'telegram_connector = chattie.connectors.telegram',
            'terminal_connector = chattie.connectors.term'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ]
)
