@echo off
SETLOCAL
SET initial_dir=%CD%

IF EXIST ".\test\" (
    echo Changing directory to: ".\test"
    cd "test"
)

echo [32m
echo Test: all commands [0m
..\dist\assembly.exe -s prog1.yaml -o prog -t

echo [32m
echo Expected: [0m
echo 0: 0x2B, 0x96, 0x28
echo 1: 0xBC, 0x2C, 0x02, 0x00, 0x00
echo 2: 0xD3, 0x0A
echo 3: 0xD9, 0x7E, 0x09, 0x00, 0x00, 0x09

cd %initial_dir%
ENDLOCAL

echo [32m
echo Test completed [0m