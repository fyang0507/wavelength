from setuptools import setup, find_packages

setup(
    name="personal_tldr",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "loguru",
        "python-dotenv",
        "requests",
        "google-api-python-client",
    ],
    extras_require={
        "openai": ["openai"],
        "claude": ["anthropic"],
        "notion": ["notion-client"],
        "dev": ["jupyterlab"]
    },
    python_requires=">=3.12",
    description="A personal TLDR tool for subscribed contents",
) 