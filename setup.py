from setuptools import setup

if __name__ == "__main__": 
   setup()

setup(
    name='chatGIT',
    version='0.1',
    scripts=['src/chatGIT'], #if no src, cannot find files.
    entry_points={
        'console_scripts': [
            'chatGIT = chatGIT:main',
        ],
    },
    install_requires=[  # List your package dependencies here
        # Example: 'requests',
    ],
)
