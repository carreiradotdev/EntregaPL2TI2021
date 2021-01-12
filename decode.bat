@echo off
title Decompressing image files

cls
echo Decoding landscape
decode.py data\compressed\lzma\landscape
echo ==================================
echo Decoding zebra
decode.py data\compressed\lzma\zebra
echo ==================================
echo Decoding egg
decode.py data\compressed\lzma\egg
echo ==================================
echo Decoding pattern
decode.py data\compressed\lzma\pattern

pause