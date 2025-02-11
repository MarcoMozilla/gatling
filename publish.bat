@echo off
chcp 65001 >nul  REM 设置 CMD 使用 UTF-8 编码，避免字符显示问题

echo Updating pip and dependencies...
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel twine pipreqs requests packaging

echo Generating requirements.txt from src...
if exist src\gatling (
    pipreqs src/gatling --force
) else (
    echo [ERROR] Directory "src/gatling" does not exist!
    pause
    exit /b 1
)

echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q *.egg-info
mkdir build
mkdir dist

echo Getting next version...
for /f %%v in ('python a_check_version.py next') do set NEW_VERSION=%%v
if "%NEW_VERSION%"=="" (
    echo [ERROR] Failed to retrieve new version from version_checker.py!
    pause
    exit /b 1
)
echo [INFO] New package version: %NEW_VERSION%

echo Building the package...
python b_setup.py sdist bdist_wheel
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo Verifying build...

REM 检查 .whl 文件是否存在
set WHL_FOUND=0
for %%F in (dist\*.whl) do set WHL_FOUND=1
if %WHL_FOUND%==0 (
    echo [ERROR] No .whl file found in dist/!
    pause
    exit /b 1
)

REM 检查 .tar.gz 文件是否存在
set TAR_FOUND=0
for %%F in (dist\*.tar.gz) do set TAR_FOUND=1
if %TAR_FOUND%==0 (
    echo [ERROR] No .tar.gz file found in dist/!
    pause
    exit /b 1
)

echo Uploading to PyPI...
twine upload dist/*
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Upload failed!
    pause
    exit /b 1
)

echo [INFO] Waiting for PyPI version update...
python a_check_version.py block

echo [SUCCESS] Update confirmed on PyPI!
pause
exit /b 0

:ERROR
echo [ERROR] PyPI version check failed!
pause
exit /b 1
