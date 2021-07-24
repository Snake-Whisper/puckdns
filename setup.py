import setuptools

__VERSION__ = '0.0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version=__VERSION__,
    name="puck-dns-api",
    author="Snake-Whisper",
    author_email="snake-whisper@web-utils.eu",
    description="Python API for the great free DNS Service \"PUCK\" from Daniel J. Luke (http://puck.nether.net/dns)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Snake-Whisper/puck-dns-api",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'requests',
    ],
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
            'source_dir': ('setup.py', 'doc')}},
)