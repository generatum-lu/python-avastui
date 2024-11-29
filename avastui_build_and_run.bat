@echo off 

rem #######################################################################   B U I L D   ####################################################################### 

:auswahl_build
set /P c=Build avastui.exe? [j/n]
if /I "%c%" EQU "j" goto :ja_build
if /I "%c%" EQU "n" goto :nein_build
goto :auswahl_build

:ja_build
echo Ja wurde gewaehlt
cd W:\Dateien\_generatum\Projekte\Python
pyinstaller --paths=subfolder python-avastui/avastui.py
:nein_build

rem #######################################################################   R U N   ####################################################################### 

:auswahl_run
set /P c=Run avastui.exe in hidden perpetual mode? [j/n]
if /I "%c%" EQU "j" goto :ja_run
if /I "%c%" EQU "n" goto :nein_run
goto :auswahl_run

:ja_run
echo Ja wurde gewaehlt
W:\Dateien\_generatum\Projekte\Python\python-avastui\nircmd-x64\nircmd.exe execmd W:\Dateien\_generatum\Projekte\Python\python-avastui\avastui.bat
:nein_run

rem #######################################################################   E N D E   ####################################################################### 
:ende

echo Alle Aufgaben sind erledigt, bitte Taste druecken zum Beenden.
pause >nul

