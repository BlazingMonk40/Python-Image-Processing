@echo off
set /p Input=Drag File Here And Press Enter:

::echo ..%Input%
If "%Input%" EQU "" goto default

python BatchResize.py %Input%
goto end

:default
echo No File Given

:end
echo END
@echo off
PAUSE