import os
import re
import shutil
from setuptools import setup, find_packages


def get_latest_version():
    """从 dist 目录读取已有的版本号，并在 PATCH 版本号上 +1"""
    dist_dir = "dist"
    version_pattern = re.compile(r"gatling-(\d+)\.(\d+)\.(\d+)\..*")
    versions = []

    if os.path.exists(dist_dir):
        for filename in os.listdir(dist_dir):
            match = version_pattern.match(filename)
            if match:
                major, minor, patch = map(int, match.groups())
                versions.append((major, minor, patch))

    if versions:
        latest_version = sorted(versions)[-1]  # 取最新版本
        major, minor, patch = latest_version
        return f"{major}.{minor}.{patch + 1}"  # PATCH +1
    else:
        return "0.1.0"  # 没有旧版本，从 0.1.0 开始


def clean_old_packages():
    """只删除 dist 目录中的旧的 gatling-*.whl 和 .tar.gz，而不是整个 dist 目录"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for filename in os.listdir(dist_dir):
            if filename.startswith("gatling-") and (filename.endswith(".whl") or filename.endswith(".tar.gz")):
                os.remove(os.path.join(dist_dir, filename))


def clean_old_gatling_dirs():
    """删除 `gatling-x.y.z` 目录"""
    base_dir = os.getcwd()  # 获取当前目录
    pattern = re.compile(r"gatling-\d+\.\d+\.\d+")  # 匹配 gatling-0.1.0 这样的目录

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and pattern.match(item):
            shutil.rmtree(item_path)  # 删除文件夹
            print(f"Deleted old package directory: {item_path}")


def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, encoding="utf-8") as f:
        return f.read()


def read_requirements():
    req_path = "src/gatling/requirements.txt"
    with open(req_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


# **先获取最新版本号**
new_version = get_latest_version()

# **删除旧的 gatling-*.whl 和 .tar.gz**
clean_old_packages()

# **删除旧的 `gatling-x.y.z` 目录**
clean_old_gatling_dirs()

setup(
    name="gatling",
    version=new_version,  # 使用最新版本号
    description="A high-performance parallel task processing framework for solving IO-bound (Redis queue, file system, command execution) and CPU-bound (computation) workloads. Designed for scalability, efficiency, and seamless distributed execution.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",  # 告诉 PyPI 这是 Markdown 格式
    author="MacroMozilla",
    author_email="honyzeng7@gmail.com",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    python_requires=">=3.10",
    url="https://github.com/MacroMozilla/gatling",
    project_urls={
        "Homepage": "https://github.com/MacroMozilla/gatling",
        "Documentation": "https://github.com/MacroMozilla/gatling/wiki",
        "Source": "https://github.com/MacroMozilla/gatling",
    },
)

