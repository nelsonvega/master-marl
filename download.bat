@echo off
REM Wrapper that runs the URL downloader from the repo root.
REM Pass-through args go straight to download_content.py.
REM
REM Examples:
REM   download.bat                              full run
REM   download.bat --limit 50                   smoke test
REM   download.bat --domains arxiv.org github.com
REM   download.bat --workers 8 --timeout 20
REM   download.bat --retry-failed

setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] python is not on PATH.
    exit /b 1
)

python src\download_content.py %*
set EXITCODE=%ERRORLEVEL%

endlocal & exit /b %EXITCODE%
