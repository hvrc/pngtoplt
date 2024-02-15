@echo off
setlocal enabledelayedexpansion

set "config_file=config.ini"    
set "input_folder="
set "output_folder="

for /f "tokens=1,2 delims==" %%a in ('type "%config_file%" ^| findstr /i "InputFolder OutputFolder"') do (
    if "%%a"=="InputFolder" (
        set "input_folder=%%b"
    ) else if "%%a"=="OutputFolder" (
        set "output_folder=%%b"
    )
)

:loop
for %%i in ("%input_folder%\*.png") do (
    set "input_file=!input_folder!\%%~ni.png"
    set "output_file=!output_folder!\%%~ni.plt"

    if not exist "%input_folder%\!output_file!" (
        echo Detected input PNG file: "!input_file!"
        pngtoplt.exe "!input_file!" "!output_file!"
        echo Converted to .plt: "!output_file!"
        del "!input_file!" /q
    )
)

timeout /t 1 /nobreak >nul
goto loop
