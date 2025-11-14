@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: compare vectors 1 [0m
..\dist\assembly.exe -s prog5_1.yaml -o ..\build\prog5_1
..\dist\interpret.exe -x ..\build\prog5_1 -d ..\build\prog5_1.mem.json -dr 0-0xFF

echo [32m
echo Test: compare vectors 1 [0m
..\dist\assembly.exe -s prog5_2.yaml -o ..\build\prog5_2
..\dist\interpret.exe -x ..\build\prog5_2 -d ..\build\prog5_2.mem.json -dr 0-0xFF

echo [32m
echo Test: compare vectors 1 [0m
..\dist\assembly.exe -s prog5_3.yaml -o ..\build\prog5_3
..\dist\interpret.exe -x ..\build\prog5_3 -d ..\build\prog5_3.mem.json -dr 0-0xFF

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m