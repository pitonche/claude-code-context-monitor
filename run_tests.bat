@echo off
REM Test runner for Claude Code Odometer Monitor

echo Running unit tests...
echo.

echo Testing token_calculator...
py tests\test_token_calculator.py
if errorlevel 1 goto error

echo.
echo Testing data_reader...
py tests\test_data_reader.py
if errorlevel 1 goto error

echo.
echo ========================================
echo All tests completed successfully!
echo ========================================
goto end

:error
echo.
echo ========================================
echo Tests failed!
echo ========================================
exit /b 1

:end
pause
