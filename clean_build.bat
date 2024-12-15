@echo off
echo Cleaning build directories...

:: 强制删除构建目录
rd /s /q build 2>nul
rd /s /q dist 2>nul
rd /s /q .pdm-build 2>nul

:: 删除所有 .egg-info 目录
for /d %%i in (*egg-info) do rd /s /q "%%i" 2>nul

echo Build directories cleaned!

:: 重新构建
echo Building package...
pdm build

echo Done!
pause