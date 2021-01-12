@echo off 

title RLE testing

cls
echo Encoding landscape.bmp
python rle_test.py data\original\landscape.bmp 
echo ==================================
echo Encoding zebra.bmp
python rle_test.py data\original\zebra.bmp 
echo ==================================
echo Encoding egg.bmp
python rle_test.py data\original\egg.bmp 
echo ==================================
echo Encoding pattern.bmp
python rle_test.py data\original\pattern.bmp

pause