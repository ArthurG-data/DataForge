from setuptools import setup
setup(
    name='DataForge',
    version = '0.1.0',
    packages=['DataForge'],
    entry_points = {
        'console-scripts': [
            'DataForge = DataForge.__main__:main'
        ]
    }
)