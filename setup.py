from setuptools import setup, find_packages

setup(
    name="helix",
    version="0.1.0",
    description="Investment platform",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[],
)
