@echo off
echo Updating pip and dependencies...
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel twine pipreqs

echo Generating requirements.txt from src...
pipreqs src/gatling --force

echo Building the package...
python setup.py sdist bdist_wheel

echo Uploading to PyPI...
twine upload dist/*

echo Done!
pause

