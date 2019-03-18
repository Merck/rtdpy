from setuptools import setup

from rtdpy.const import version

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='rtdpy',
    version=version,
    packages=['rtdpy'],
    license='LICENSE',
    author='Matthew Flamm',
    author_email='matthew.flamm@merck.com',
    description='Python package for residence time distribution analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy',
                      'scipy',],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",],
)
