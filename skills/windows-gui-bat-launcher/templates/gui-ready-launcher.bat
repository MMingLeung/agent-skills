@echo off
REM Windows GUI 交付启动模板。把 tool_hub、your_package、日志名改成当前工具。说明见 ../SKILL.md
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONPATH=%~dp0"
set PYTHONUTF8=1
set "PYTHON=%~dp0py11\python.exe"
set "READY=%~dp0output\.ready_tool_hub"
set "LOG=%~dp0output\startup_bat_hub.log"
if not exist "%~dp0output" mkdir "%~dp0output"
if exist "%READY%" del /f /q "%READY%" >nul 2>&1
echo [%DATE% %TIME%] start>"%LOG%"

echo.
echo ========================================
echo   正在启动，请稍候...
echo ========================================
echo.

if not exist "%PYTHON%" (
  echo [错误] 未找到 py11\python.exe
  pause
  exit /b 2
)
echo using python.exe>>"%LOG%"
start /B "" "%PYTHON%" -X utf8 -m your_package >>"%LOG%" 2>&1

set /a _WAIT=0
:wait_loop
if exist "%READY%" goto :ready_ok
if %_WAIT% GEQ 90 goto :ready_timeout
set /a _WAIT+=1
ping -n 2 127.0.0.1 >nul
goto :wait_loop

:ready_ok
echo 程序已打开，即将关闭本窗口。
ping -n 2 127.0.0.1 >nul
exit /b 0

:ready_timeout
echo 启动超时。请查看 output\startup_bat_hub.log
type "%LOG%"
pause
exit /b 1
