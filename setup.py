import os
import re
from setuptools import setup
from setuptools import find_packages


thorinfile = os.path.join(os.path.dirname(__file__),
                          'src', 'thorin', '__init__.py')

# Thanks to SQLAlchemy:
# https://github.com/zzzeek/sqlalchemy/blob/master/setup.py#L104
with open(thorinfile) as stream:
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
    name='thorin',
    description='A framework for making bots in Python.',
    version=__version__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author="""
Mathew Robinson <mrobinson@praelatus.io>
    """,
    download_url='https://github.com/chasinglogic/Thorin/releases',
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'thorin = thorin.cli:thorin'
        ],
        'thorin.plugins.tricks': [
            'default_tricks = thorin.tricks',
        ],
        'thorin.plugins.connectors': [
            'telegram_connector = thorin.connectors.telegram',
            'terminal_connector = thorin.connectors.term'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Bug Tracking',
    ]
)
