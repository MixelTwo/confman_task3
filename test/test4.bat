@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: bin_eq [0m
..\dist\assembly.exe -s prog3.yaml -o ..\build\prog3
..\dist\interpret.exe -x ..\build\prog3 -d ..\build\prog3.mem.json -dr 0-0xFF -t

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m