# version_checker.py
import os
import re
import time
import requests
from packaging.version import Version

from z_setup import a_const
from z_setup.a_const import PACKAGE_NAME


def get_remote_version(package_name):
    """获取 PyPI 上的最新版本号"""
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(pypi_url, timeout=5)
        response.raise_for_status()
        versions = sorted(response.json()["releases"].keys(), key=Version)
        return versions[-1]
    except (requests.RequestException, KeyError, IndexError):
        return None


def get_local_version(package_name):
    """获取本地 dist/ 目录中的最新版本号"""
    version_pattern = re.compile(rf"{package_name}-(\d+)\.(\d+)\.(\d+)\..*")
    dist_dir = "dist"
    versions = [
        tuple(map(int, match.groups()))
        for filename in os.listdir(dist_dir)
        if (match := version_pattern.match(filename))
    ] if os.path.exists(dist_dir) else []

    return ".".join(map(str, sorted(versions)[-1])) if versions else None


def gen_next_version(latest_version):
    """计算下一个版本号（PATCH +1）"""
    if latest_version:
        major, minor, patch = map(int, latest_version.split("."))
        return f"{major}.{minor}.{patch + 1}"
    return "0.1.0"


def compare_versions_and_block(package_name):
    """等待远程 PyPI 版本更新"""
    print("🔄 Checking version updates...")
    while True:
        local_version = get_local_version(package_name)
        remote_version = get_remote_version(package_name)

        if local_version is None or remote_version is None:
            print("⚠️  Failed to get version info, retrying...")
        elif Version(local_version) == Version(remote_version):
            print(f"\n✅ Versions are synchronized: {local_version}")
            break
        else:
            print(".", end="", flush=True)
            time.sleep(1)  # 每秒检查一次

    print("\n Update complete!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python version_checker.py remote")
        print("  python version_checker.py local")
        print("  python version_checker.py next")
        print("  python version_checker.py block")
        sys.exit(1)

    command = sys.argv[1]

    if command == "remote":
        print(get_remote_version(package_name=PACKAGE_NAME))

    elif command == "local":
        print(get_local_version(package_name=PACKAGE_NAME))

    elif command == "next":
        print(gen_next_version(get_remote_version(package_name=PACKAGE_NAME)))

    elif command == "block":
        compare_versions_and_block(package_name=PACKAGE_NAME)

    else:
        print("⚠️  Unknown command! Use 'remote', 'local', 'next', or 'block'")
        sys.exit(1)
