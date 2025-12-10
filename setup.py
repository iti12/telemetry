from setuptools import setup, find_packages

setup(
    name="telemetry",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.0",
        "pyyaml>=6.0",
        "redis>=5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
            "pytest-aiohttp>=1.0",
            "pytest-asyncio>=0.23",
        ]
    },
    entry_points={
        "console_scripts": [
            "telemetry-generator=telemetry_generator.main:main",
        ]
    },
)
