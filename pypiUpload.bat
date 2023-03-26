@echo off
setlocal EnableDelayedExpansion

set VERSION=

for /f "tokens=3" %%a in ('findstr "version =" setup.py') do set VERSION=%%~a

if not defined VERSION (
    echo Error: could not find version number in setup.py.
    exit /b 1
)

echo Uploading ai_header_generator version %VERSION% to PyPI...
twine upload dist/ai_header_generator-%VERSION%.tar.gz -u __token__ -p your_token_here

if errorlevel 1 (
    echo Error: failed to upload package to PyPI.
    exit /b 1
)

echo Upload complete.