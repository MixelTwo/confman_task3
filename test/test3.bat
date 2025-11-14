@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: copy array from 80-85 to 96-101 [0m
..\dist\assembly.exe -s prog2.yaml -o ..\build\prog2
..\dist\interpret.exe -x ..\build\prog2 -d ..\build\prog2.mem.json -dr 0-0xFF -t

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m