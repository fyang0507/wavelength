from setuptools import setup, find_packages

setup(
    name="wavelength",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "loguru",
        "python-dotenv",
        "requests",
        "google-api-python-client",
        "openai",
        "anthropic",
        "notion-client",
    ],
    extras_require={
        "dev": ["jupyterlab"]
    },
    python_requires=">=3.12",
    description="A content curation tool that filters subscriptions using AI to deliver only meaningful content that matters to you",
) 