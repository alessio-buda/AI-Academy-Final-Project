@echo off
REM Windows batch file for building Sphinx documentation
REM This is the Windows equivalent of the Unix Makefile

if "%1" == "" goto help

if "%1" == "help" goto help
if "%1" == "clean" goto clean
if "%1" == "html" goto html
if "%1" == "serve" goto serve
if "%1" == "install" goto install
if "%1" == "watch" goto watch

goto help

:help
echo AI Academy Report Generator Documentation
echo ==========================================
echo.
echo Available commands:
echo   help      Show this help message
echo   install   Install documentation dependencies
echo   clean     Clean build directory
echo   html      Build HTML documentation
echo   serve     Serve documentation locally
echo   watch     Live reload development server
echo.
echo Examples:
echo   make.bat install
echo   make.bat html
echo   make.bat serve
goto end

:install
echo Installing documentation dependencies...
python -m pip install -r requirements-docs.txt
if errorlevel 1 goto error
echo Dependencies installed successfully!
goto end

:clean
echo Cleaning build directory...
if exist "_build" rmdir /s /q "_build"
echo Build directory cleaned!
goto end

:html
echo Building HTML documentation...
sphinx-build -b html source _build\html
if errorlevel 1 goto error
echo.
echo HTML documentation built successfully!
echo Open _build\html\index.html in your browser
goto end

:serve
echo Building and serving documentation...
if not exist "_build\html" (
    echo Building documentation first...
    sphinx-build -b html source _build\html
    if errorlevel 1 goto error
)
echo.
echo Starting local server at http://localhost:8000
echo Press Ctrl+C to stop the server
cd _build\html
python -m http.server 8000
goto end

:watch
echo Starting live reload development server...
echo Press Ctrl+C to stop
sphinx-autobuild source _build\html --host 127.0.0.1 --port 8000
goto end

:error
echo.
echo Error occurred! Please check the output above.
exit /b 1

:end
