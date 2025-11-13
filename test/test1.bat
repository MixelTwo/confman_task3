@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: wrong args [0m
..\dist\assembly.exe

echo [32m
echo Test: unexisting input file [0m
..\dist\assembly.exe -s not_exist.yaml -o prog

echo [32m
echo Test: wrong format config [0m
..\dist\assembly.exe -s prog_bad.yaml -o prog

echo [32m
echo Test: all correct [0m
..\dist\assembly.exe -s prog1.yaml -o prog

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m