@echo off
::runas administrator
%1 start "" mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
setlocal enabledelayedexpansion
call :setdir
call :configx86orx64
set "pythondir=c:\python27"
set "libboostdir=c:\local\boost_1_68_0"
set "logfile=%~dp0\UnInstallLog.txt"
set extract=extract
echo ------------------------------------------------------
echo                 Uninstalling python27
echo ------------------------------------------------------
call :uninstallmsiPackage "%python27Name%" "%python27Name%"
if exist %pythondir%  rmdir /s /q %pythondir%
if exist %pythondir%  rd /s /q %pythondir%
set delPythonPath=%PATH:;c:\python27=%
set delPythonExt=%PATHEXT:;.PY;.PYM=%
wmic ENVIRONMENT where "name='PATH' and username='<system>'" set VariableValue="%delPythonPath%"
wmic ENVIRONMENT where "name='PATHEXT' and username='<system>'" set VariableValue="%delPythonExt%"
echo ------------------------------------------------------
echo                 Uninstalling libboost
echo ------------------------------------------------------
if exist %libboostdir% rd /s /q %libboostdir%
echo ------------------------------------------------------
echo                 Uninstalling ffmpeg  
echo ------------------------------------------------------
if exist %extract% rd /s /q %extract%
echo ------------------------------------------------------
echo              Cleaning downloaded files
echo ------------------------------------------------------
del /f /q %pythonPackage%
del /f /q %pipPackage%
del /f /q %ffmpegPackage%
del /f /q %libboostPackage%
echo ------------------------------------------------------
echo                 Uninstallation done.          
echo ------------------------------------------------------
pause
goto :eof

::-----------------下面是目录切换定义区域-----------------
::在管理员模式执行时，默认路径变更，此处将目录切换回来
:setdir
set char=%~dp0%
%char:~0,2%
cd  %~dp0%
goto :eof

::-----------------下面是版本函数定义区域-----------------
:configx86orx64
IF %PROCESSOR_ARCHITECTURE% == AMD64 (
	set versionFlag=win64
) else ( 
	set versionFlag=win32
)

echo Windows Version: %versionFlag%
if %versionFlag%==win64 (
	set "python27Name=python 2.7.15 (64-bit)"
	set "python27ProductCode=20C31435-2A0A-4580-BE8B-AC06FC243CA5"
	set pythonPackage=python-2.7.15.amd64.msi
	set pipPackage=get-pip.py
	set ffmpegPackage=ffmpeg-20180825-844ff49-win64-shared.zip
	set libboostPackage="boost_1_68_0-msvc-12.0-64.exe"
) else (
	set "python27Name=Python 2.7.15"
	set "python27ProductCode=20C31435-2A0A-4580-BE8B-AC06FC243CA4"
	set pythonPackage=python-2.7.15.msi
	set pipPackage=get-pip.py
	set ffmpegPackage=ffmpeg-20180825-844ff49-win32-shared.zip
	set libboostPackage="boost_1_68_0-msvc-12.0-32.exe"
)
endlocal
goto :eof

::-----------------下面是卸载函数定义区域-----------------
:uninstallmsiPackage
echo Strat uninstalling "%~2"...
echo "%~2" Start...%date% %time%>>%logfile%
FOR /f "tokens=1" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /e /s /d /f "%~2"^|FINDSTR /i "CurrentVersion"') do (
	FOR /f "tokens=1-2,*" %%j in ('reg query "%%i" /f "UninstallString"^|FINDSTR /i "UninstallString"') do (
		set correct=%%l && set correct=!correct:/I{=/passive /norestart /x{! && CMD /q /c "!correct!"
	)
)

IF %ERRORLEVEL% EQU 0 echo Uninstall %~2 Successfull
IF %ERRORLEVEL% NEQ 0 IF %ERRORLEVEL% NEQ 1605 echo Uninstall %~2 Failed, ERRORLEVEL:%ERRORLEVEL%.
echo ERRORLEVEL:%ERRORLEVEL%>>%logfile%
echo %~2 End %date% %time%>>%logfile%
echo -----------------------------------------------------
goto :eof