from setuptools import setup, find_packages

setup(
    name="driftmonitor",
    version="1.0.0",
    description="AI Safety & Risk Drift Monitoring Platform",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0",
        "pytrends>=4.9.0",
        "PyYAML>=6.0",
    ],
    python_requires=">=3.10",
)
