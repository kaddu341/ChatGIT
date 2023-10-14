from setuptools import setup

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()

setup(
    name='chatGIT',
    version='0.1',
    py_modules=['chatGIT'],
    entry_points={
        'console_scripts': [
            'chatGIT = chatGIT:main',
        ],
    },
    install_requires=[  # List your package dependencies here
        # Example: 'requests',
    ],
)
