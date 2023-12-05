# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="k4Generators",  # Required
    version="alpha",  # Required
    description="A python module for creating Monte-Carlo generator cards",  # Optional
    # long_description=long_description,  # Optional
    # long_description_content_type="text/markdown",  # Optional (see note above)
    # url="https://github.com/pypa/sampleproject",  # Optional
    author="Alan Price",  # Optional
    author_email="alan.price[at]cern.ch",  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Build Tools",
        # "License :: OSI Approved :: MIT License",
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    # keywords="sample, setuptools, development",  # Optional
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7, <4",
    install_requires=["shutil","sys", "os", "argparse"],  # Optional
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     "sample": ["package_data.dat"],
    # },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    project_urls={  # Optional
        "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        # "Funding": "https://donate.pypi.org",
        # "Say Thanks!": "http://saythanks.io/to/example",
        # "Source": "https://github.com/pypa/sampleproject/",
    },
)