@ECHO off
set cl=%1

TITLE Compressing images...

cls
ECHO =================================
ECHO ^| Delta Encoding + BZip2 - CL %cl% ^|
ECHO =================================
ECHO.

ECHO Encoding landscape.bmp
python bzip2.py data\original\landscape.bmp %cl%

ECHO ==================================

ECHO Encoding zebra.bmp
python bzip2.py data\original\zebra.bmp %cl%

ECHO ==================================

ECHO Encoding egg.bmp
python bzip2.py data\original\egg.bmp %cl%

ECHO ==================================

ECHO Encoding pattern.bmp
python bzip2.py data\original\pattern.bmp %cl%

PAUSE