# setup.py

from setuptools import setup, find_packages

setup(
    name="reliability",
    version="0.1.0",
    description="A reliability parts repository as defined in MIL-STD-217",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/reliability",  # Update with your repository URL
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # List dependencies here, e.g., "numpy>=1.21.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            # If you want a command-line interface, you can define an entry point.
            "reliability= reliability.main:main",
        ],
    },
    python_requires=">=3.6",
)
