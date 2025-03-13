from setuptools import setup, find_packages

setup(
    name="reliability",
    version="0.1.0",
    description="A reliability parts repository tool for MIL-STD-217 analysis",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/reliability",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas",
        "openpyxl",
        "xlsxwriter",
        "streamlit",
        "requests",
        "beautifulsoup4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "reliability= reliability.ui:main",
        ],
    },
    python_requires=">=3.6",
)

