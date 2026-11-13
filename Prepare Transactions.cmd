@echo off
setlocal
pushd "%~dp0" || exit /b 1
set "converter_python=.venv\Scripts\python.exe"

if not exist "%converter_python%" (
    py -3.12 -m venv .venv 2>nul
    if errorlevel 1 (
        python -c "import sys; sys.exit(not ((3, 9) <= sys.version_info[:2] <= (3, 13)))"
        if errorlevel 1 (
            echo Python 3.12 is recommended. Install it from python.org and run this again.
            goto failed
        )
        python -m venv .venv || goto failed
    )
)

"%converter_python%" -c "import pandas; raise SystemExit(pandas.__version__ != '2.2.3')" 2>nul
if errorlevel 1 (
    "%converter_python%" -m pip install -r requirements-conversion.txt || goto failed
)

"%converter_python%" src\convert_transactions.py || goto failed
explorer "%CD%\data\processed"
popd
pause
exit /b 0

:failed
popd
pause
exit /b 1
