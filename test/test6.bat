@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: sum [0m
..\dist\assembly.exe -s prog6_1.yaml -o ..\build\prog6_1
..\dist\interpret.exe -x ..\build\prog6_1 -d ..\build\prog6_1.mem.json -dr 0-0xFF

echo [32m
echo Test: jump (calc sum of 1+2+3+...+10) [0m
..\dist\assembly.exe -s prog6_2.yaml -o ..\build\prog6_2
..\dist\interpret.exe -x ..\build\prog6_2 -d ..\build\prog6_2.mem.json -dr 0-0xFF

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m