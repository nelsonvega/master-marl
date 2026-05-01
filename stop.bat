@echo off
REM Signal the running downloader to stop cleanly.
REM Creates a STOP sentinel file in the repo root. The downloader checks for
REM it before scheduling each new task and exits gracefully when it appears.
REM
REM Hard stop alternative: press Ctrl+C in the running window (handled too).

setlocal
cd /d "%~dp0"
echo stop requested at %DATE% %TIME% > STOP
echo [stop.bat] STOP file created at %CD%\STOP
echo [stop.bat] The downloader will exit after current in-flight tasks finish.
endlocal
