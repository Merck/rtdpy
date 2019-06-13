from setuptools import setup

exec(open('rtdpy/version.py').read())

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='rtdpy',
    version=__version__,
    packages=['rtdpy'],
    license='LICENSE',
    author='Matthew Flamm',
    author_email='matthew.flamm@merck.com',
    url='https://merck.github.io/rtdpy',
    description='Python package for residence time distribution analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy',
                      'scipy'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        ],
)
