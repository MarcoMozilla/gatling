import os
import shutil
from setuptools import setup, find_packages

# **导入 version_checker 逻辑**
from a_check_version import *

# **清理旧的 `dist/` 目录**
shutil.rmtree("dist", ignore_errors=True)

# **获取最新版本号**
new_version = gen_next_version(get_remote_version())
print(f"🔹 New package version: {new_version}")


def read_long_description():
    """读取 `README.md` 作为 `long_description`"""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def read_requirements():
    """读取 `requirements.txt`"""
    with open("src/gatling/requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def clean_packages():
    """删除 `dist/` 目录中的旧的 `.whl` 和 `.tar.gz`"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for filename in os.listdir(dist_dir):
            if filename.startswith("gatling-") and (filename.endswith(".whl") or filename.endswith(".tar.gz")):
                os.remove(os.path.join(dist_dir, filename))


def clean_dirs():
    """删除 `gatling-x.y.z` 目录，等待文件解除占用"""
    base_dir = os.getcwd()
    pattern = re.compile(f"{PACKAGE_NAME}-\\d+\\.\\d+\\.\\d+")

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and pattern.match(item):
            print(f"🔄 Attempting to delete: {item_path}")
            retries = 5  # 最多尝试 5 次

            for attempt in range(retries):
                try:
                    shutil.rmtree(item_path)
                    print(f"✅ Deleted: {item_path}")
                    break  # 删除成功，退出循环
                except PermissionError:
                    print(f"⚠️  Delete failed (attempt {attempt + 1}/{retries}), retrying in 2 seconds...")
                    time.sleep(2)  # 等待 2 秒后重试
            else:
                print(f"❌ Failed to delete {item_path}, it might be locked!")


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

clean_dirs()
