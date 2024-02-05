from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sippycup',
    version='0.1.0',
    description='A sip client',
    long_description=readme,
    author='Jake Robers',
    author_email='jake@jakerobers.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
