@echo off


if "%1"=="" (
    set preset=6
) else (
    set preset=%1
)

title Compressing images...

cls
echo ====================================
echo ^| Delta Encoding + LZMA - Preset %preset% ^|
echo ====================================
echo.

echo Encoding landscape.bmp
python encode.py data\original\landscape.bmp %preset%
echo ==================================
echo Encoding zebra.bmp
python encode.py data\original\zebra.bmp %preset%
echo ==================================
echo Encoding egg.bmp
python encode.py data\original\egg.bmp %preset%
echo ==================================
echo Encoding pattern.bmp
python encode.py data\original\pattern.bmp %preset%

pause