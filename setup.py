from setuptools import setup, find_packages


# 读取 requirements.txt
def read_requirements():
    with open("src/gatling/requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="gatling",
    version="0.1.0",
    description="A high-performance parallel task processing framework for solving IO-bound (Redis queue, file system, command execution) and CPU-bound (computation) workloads. Designed for scalability, efficiency, and seamless distributed execution.",
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

