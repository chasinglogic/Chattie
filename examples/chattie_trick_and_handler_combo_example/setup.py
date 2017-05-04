from setuptools import setup
from setuptools import find_packages

setup(
    name='chattie trick and handler combo example',
    description='An example on how to write your own handlers and tricks in the same package.',
    packages=find_packages(),
    author="""
Mathew Robinson <mrobinson@praelatus.io>
    """,
    install_requires=[
        'chattie'
    ],
    entry_points={
        'chattie.plugins.handlers': [
            'example_handlers_combo = chattie_trick_and_handler_combo_example.handlers'
        ],
        'chattie.plugins.tricks': [
            'example_tricks_combo = chattie_trick_and_handler_combo_example.tricks'
        ]
    },
    license='Apache2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ]
)
