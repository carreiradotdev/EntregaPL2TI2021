@echo off

if "%1"=="" (
    set preset=6
) else (
    set preset=%1
)

title Compressing images...

cls
echo Encoding landscape.bmp
python zlib_test.py data\original\landscape.bmp %preset%
echo ==================================
echo Encoding zebra.bmp
python zlib_test.py data\original\zebra.bmp %preset%
echo ==================================
echo Encoding egg.bmp
python zlib_test.py data\original\egg.bmp %preset%
echo ==================================
echo Encoding pattern.bmp
python zlib_test.py data\original\pattern.bmp %preset%

pause