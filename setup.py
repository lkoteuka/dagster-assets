from setuptools import find_packages, setup

setup(
    name="dagster_assets",
    packages=find_packages(exclude=["dagster_assets_tests"]),
    install_requires=[
        "dagster==1.5.13",
        "dagster-webserver==1.5.13",
        "pandas==2.1.4",
        "numpy==1.26.2",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
