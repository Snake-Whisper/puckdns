import setuptools
import os

__VERSION__ = 'N/A'

if 'PUCKDNS_BUILD_VERSION' in os.environ:
    __VERSION__ = os.getenv('PUCKDNS_BUILD_VERSION')
elif 'GITHUB_REF_TYPE' in os.environ:
    ref_type = os.getenv('GITHUB_REF_TYPE')
    if ref_teype == 'tag' and 'GITHUB_REF_NAME' in os.environ:
        __VERSION__ = os.getenv('GITHUB_REF_NAME')
    elif ref_type == 'branch' and 'GITHUB_SHA' in os.environ:
        __VERSION__ = os.getenv('GITHUB_SHA')
    

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version=__VERSION__,
    name="puckdns",
    author="Snake-Whisper",
    author_email="snake-whisper@web-utils.eu",
    description="Python API for the great free DNS Service \"PUCK\" from Daniel J. Luke (http://puck.nether.net/dns)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Snake-Whisper/puckdns",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=3.6',
    command_options={
        'build_sphinx': {
            'version': ('setup.py', __VERSION__),
            'release': ('setup.py', __VERSION__),
            'source_dir': ('setup.py', 'docs')}},
)