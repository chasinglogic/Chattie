from setuptools import setup
from setuptools import find_packages

setup(
    name='chattie trick example',
    description='An example on how to write your own tricks.',
    packages=find_packages(),
    author="""
Mathew Robinson <mrobinson@praelatus.io>
    """,
    install_requires=[
        'chattie'
    ],
    entry_points={
        'chattie.plugins.tricks': [
            'example_tricks = chattie_trick_example'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ]
)
