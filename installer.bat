@echo off
py -m pip install spotipy
py -m pip install Pillow
cd /D "%~dp0"
XCOPY ".\SpotiShuffler.lnk" "%AppData%\Microsoft\Windows\Start Menu" /D
echo.
echo.
echo Installation complete
echo.
set /P askLaunch=Do you want to launch SpotiShuffler [Y/N]?
if %askLaunch% == Y pyw ".\spotiShuffler.pyw"
exit