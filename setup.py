import os
import re
import shutil
import requests
from packaging.version import Version
from setuptools import setup, find_packages


def get_latest_version_from_pypi(package_name="gatling"):
    """从 PyPI 获取最新版本号"""
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(pypi_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        versions = sorted(data["releases"].keys(), key=Version)
        latest_version = versions[-1]
        print(f"Latest version on PyPI: {latest_version}")
        return latest_version
    except (requests.RequestException, KeyError, IndexError):
        print("⚠️  Failed to fetch latest version from PyPI, falling back to local dist directory.")
        return None


def get_latest_version():
    """获取最新版本号，优先从 PyPI 获取，如果失败则从本地 dist 目录获取"""
    latest_version = get_latest_version_from_pypi()

    if latest_version is None:
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
            latest_version = ".".join(map(str, sorted(versions)[-1]))  # 取最新版本
        else:
            latest_version = "0.1.0"  # 没有旧版本，从 0.1.0 开始

    # 解析并 +1 版本号
    major, minor, patch = map(int, latest_version.split("."))
    return f"{major}.{minor}.{patch + 1}"  # PATCH +1


def clean_packages():
    """删除 `dist/` 目录中的旧的 `.whl` 和 `.tar.gz`"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for filename in os.listdir(dist_dir):
            if filename.startswith("gatling-") and (filename.endswith(".whl") or filename.endswith(".tar.gz")):
                os.remove(os.path.join(dist_dir, filename))


def clean_gatling_dirs():
    """删除 `gatling-x.y.z` 目录"""
    base_dir = os.getcwd()
    pattern = re.compile(r"gatling-\d+\.\d+\.\d+")

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and pattern.match(item):
            shutil.rmtree(item_path)
            print(f"Deleted old package directory: {item_path}")


def read_long_description():
    """读取 README.md 作为 long_description"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, encoding="utf-8") as f:
        return f.read()


def read_requirements():
    """读取 requirements.txt"""
    req_path = "src/gatling/requirements.txt"
    with open(req_path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


# **获取最新版本号**
new_version = get_latest_version()
print(f"🔹 New package version: {new_version}")

# **清理旧的构建文件**
clean_packages()

setup(
    name="gatling",
    version=new_version,  # 使用最新版本号
    description="A high-performance parallel task processing framework for solving IO-bound (Redis queue, file system, command execution) and CPU-bound (computation) workloads. Designed for scalability, efficiency, and seamless distributed execution.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="MacroMozilla",
    author_email="honyzeng7@gmail.com",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    options={"egg_info": {"egg_base": "build"}},
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

clean_gatling_dirs()
