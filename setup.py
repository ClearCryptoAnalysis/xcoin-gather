"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="xcoingather",
    version="0.0.4",
    description="Data gathering tools for various crypto coins.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://medium.com/@clearcryptoanalysis",
    author="Clear Crypto Analysis",
    author_email="canadacryptofacts.gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    project_urls={
        "Clear Crypto Analysis": "https://medium.com/@clearcryptoanalysis",
        "Source": "https://github.com/pypa/sampleproject/",
    },
)
