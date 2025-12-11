from setuptools import setup, find_packages

setup(
    name="driftmonitor",
    version="0.1.0",
    description="AI Drift & Safety Monitoring System (Lightweight, GitHub-native)",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "pytrends>=4.8.0",
        "pandas>=2.0",
        "PyYAML>=6.0",
        "pytest>=7.0",
        "requests>=2.28",
        "transformers>=4.30.0",
        "torch>=1.13.0",
        "jinja2>=3.1.0",
    ],
)
