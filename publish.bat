@echo off
echo Updating pip and dependencies...
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel twine pipreqs

echo Generating requirements.txt from src...
if exist src\gatling (
    pipreqs src/gatling --force
) else (
    echo ❌ ERROR: Directory "src/gatling" does not exist!
    pause
    exit /b 1
)

echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q *.egg-info
mkdir build
mkdir dist

echo Building the package...
python setup.py sdist bdist_wheel
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Build failed!
    pause
    exit /b 1
)

echo Verifying build...
if not exist "dist\*.whl" (
    echo ❌ ERROR: No .whl file found in dist/!
    pause
    exit /b 1
)

if not exist "dist\*.tar.gz" (
    echo ❌ ERROR: No .tar.gz file found in dist/!
    pause
    exit /b 1
)

echo Uploading to PyPI...
twine upload dist/*
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Upload failed!
    pause
    exit /b 1
)

echo ✅ Done!
pause
