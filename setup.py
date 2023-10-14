import setuptools
setuptools.setup(
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
