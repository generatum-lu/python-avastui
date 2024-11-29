:: :: https://superuser.com/questions/1362291/auto-restart-an-executable-after-the-application-crashes
:: @echo off
:: :Start
:: C:\path\to\application.exe
:: :: Wait 30 seconds before restarting.
:: TIMEOUT /T 30
:: GOTO:Start


:: W:\Dateien\_generatum\Projekte\Python\python-avastui\nircmd-x64\nircmd.exe execmd W:\Dateien\_generatum\Projekte\Python\python-avastui\avastui.bat

@ECHO off
SET _PollingInterval=10

:BatchStart
W:\Dateien\_generatum\Projekte\Python\python-avastui\nircmd-x64\nircmd.exe execmd W:\Dateien\_generatum\Projekte\Python\dist\avastui\avastui.exe

:Start
:: Uncomment the following line on versions of Windows prior to Windows 7 and comment out the TIMEOUT line. The PING solution will not be 100% accurate with _PolingInterval.
:: PING 127.0.0.1 -n %_PollingInterval% >nul
TIMEOUT /T %_PollingInterval%

SET PID=
FOR /F "tokens=2 delims= " %%i IN ('TASKLIST ^| FIND /i "avastui.exe"') DO SET PID=%%i
IF [%PID%]==[] (
    ECHO Application was not running. Restarting script.
    GOTO BatchStart
)
GOTO Start

GOTO:EOF