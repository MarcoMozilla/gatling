import os

from setuptools import setup, find_packages


def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, encoding="utf-8") as f:
        return f.read()


def read_requirements():
    with open("src/gatling/requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="gatling",
    version="0.1.0",
    description="A high-performance parallel task processing framework for solving IO-bound (Redis queue, file system, command execution) and CPU-bound (computation) workloads. Designed for scalability, efficiency, and seamless distributed execution.",
    long_description=read_long_description(),
    author="MacroMozilla",
    author_email="honyzeng7@gmail.com",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),  # 读取 requirements.txt
    python_requires=">=3.10",
    url="https://github.com/MacroMozilla/gatling",
    project_urls={
        "Homepage": "https://github.com/MacroMozilla/gatling",
        "Documentation": "https://github.com/MacroMozilla/gatling/wiki",
        "Repository": "https://github.com/MacroMozilla/gatling",
    },
)
