from setuptools import setup, find_packages

setup(
    name="ai_header_generator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "ai-header-generator=cli:main",
        ],
    },
)