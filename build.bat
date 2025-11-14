pyinstaller assembly.spec --workpath ./build
pyinstaller interpret.spec --workpath ./build
rd build /S /Q