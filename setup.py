from pathlib import Path

from setuptools import setup  # pyright: reportMissingTypeStubs=false

from stackwhy.version import get_version

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Software Development :: Testing",
    "Topic :: Utilities",
    "Typing :: Typed",
]

version = get_version()

if "a" in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="CLI tool and package for visualising the most recent events on an Amazon Web Services CloudFormation stack",
    entry_points={
        "console_scripts": [
            "stackwhy=stackwhy.__main__:cli_entry",
        ],
    },
    include_package_data=True,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="stackwhy",
    packages=[
        "stackwhy",
        "stackwhy.version",
    ],
    package_data={
        "stackwhy": ["py.typed"],
        "stackwhy.version": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/stackwhy",
    version=version,
)
