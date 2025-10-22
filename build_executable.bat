@echo off
REM ============================================================================
REM Build Standalone Executable for Bank Transaction Analyzer
REM ============================================================================

echo.
echo ============================================================================
echo Building Bank Transaction Analyzer Executable
echo ============================================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not found!
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [1/3] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] Building executable (this may take 5-10 minutes)...
pyinstaller --clean build_simple.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo [3/3] Creating release package...
if not exist release mkdir release
copy dist\BankTransactionAnalyzer.exe release\
copy README_USER.md release\

echo.
echo ============================================================================
echo BUILD SUCCESSFUL!
echo ============================================================================
echo.
echo Executable location: release\BankTransactionAnalyzer.exe
echo User guide: release\README_USER.md
echo.
echo Next steps:
echo 1. Test the executable: cd release ^&^& BankTransactionAnalyzer.exe
echo 2. Zip the release folder for distribution
echo 3. Share with users (they only need Ollama installed)
echo.
echo ============================================================================

pause
