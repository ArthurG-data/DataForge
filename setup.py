from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name='DataForge',
    version = '0.2.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    include_package_data=True,
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
    python_requires='>=3.11.5', 
)