::@echo off
set /p Input=Drag File Here And Press Enter:

::echo ..%Input%
If "%Input%" EQU "" goto default

python3 "%~dp0BatchResize.py" %Input%
PAUSE
goto end

:default
echo No File Given

:end
echo END
@echo off
PAUSE