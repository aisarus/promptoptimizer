@echo off
echo ========================================
echo  RESET DEV VERSION
echo ========================================
echo.
echo WARNING: This will DELETE all changes in DEV version
echo and restore from the PRODUCTION backup.
echo.
echo Current folder: %CD%
echo.
echo Press Ctrl+C to CANCEL
echo Press any key to CONTINUE and RESET...
pause >nul
echo.

echo Deleting current DEV folder...
cd ..
rmdir /S /Q prompt-optimizer-saas-dev

echo Creating fresh copy from PRODUCTION...
xcopy prompt-optimizer-saas prompt-optimizer-saas-dev /E /I /H /Q

echo.
echo ========================================
echo  DEV version has been RESET!
echo ========================================
echo.
echo Fresh copy created from production version.
echo All your experimental changes have been removed.
echo.
echo NOTE: You need to update ports manually or
echo re-extract the DEV archive.
echo.

pause
