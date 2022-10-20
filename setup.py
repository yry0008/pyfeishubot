import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PYfeishuBot",
    version="0.0.2",
    author="Yang",
    author_email="plectra-taproot0y@icloud.com",
    description="A feishu Bot SDK for Python",
    keywords='feishu lark bot api tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yry0008/pyfeishubot.git",
    packages=setuptools.find_packages(exclude = ['tests', 'examples']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.28.0",
        "fastapi>=0.78.0",
        "uvicorn>=0.17.6",
        "pycryptodome>=3.14.1"
    ]
)