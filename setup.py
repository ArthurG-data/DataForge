from setuptools import setup

setup(
    name='DataForge',
    version = '0.1.0',
    packages=['DataForge'],
    entry_points = {
        'console_scripts': [
            'DataForge = DataForge.__main__:run_cli'
        ]
    },
    author="Arthur Guillaume",
    description="A companion package for database creation and management",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.5',  # Adjust as needed
)