# Entropies
Original

    landscape: 7.420784
    zebra: 5.831376
    egg: 5.724301
    pattern: 1.829457

Delta Encoded 1x

    landscape: 2.824984
    zebra: 3.222192
    egg: 2.700172
    pattern: 0.595832
    
Delta Encoded 2x

    landscape: 3.090073
    zebra: 3.272709
    egg: 2.893933
    pattern: 0.714130

Move-to-Front

    landscape: 3.465445
    zebra: 4.330849
    egg: 3.417975
    pattern: 0.617801

RLE

    file: runs | lengths
    landscape: 5.008738 | 1.312405
    zebra: 4.093816 |  1.240050
    egg: 3.837112 | 1.195398
    pattern: 0.521089 | 0.337420

BWT não foi testado pois a implementações existentes visam strings, não bytes. Modificar as existentes para usar bytes não era fácil, nem implementar com código próprio para usar bytes.

# Compression ratios

! Escolhemos Delta Encoding por ser de fácil implementação e rápida execução !

Delta + BZip2

    file: compression ratio | execution time
    landscape: 3.32 | 4.25s
    zebra: 2.85 | 7.27s
    egg: 3.69 | 7.25s
    pattern: 22.62 | 17.34s

Delta + LZMA 

    file: compression ratio | execution time
    landscape: 4.04 | 24.74s
    zebra: 3.22 | 37.57s
    egg: 4.25 | 32.67s
    pattern: 22.32 | 38.47s

RLE + LZMA

    file: compression ratio | execution time
    landscape: 2.74 | 58.63s
    zebra: 2.49 | 66.61s
    egg: 3.13 | 66.22s
    pattern: 25.12 | 30.28s

MTF + RLE + LZMA

    It's even worse than RLE + LZMA
    Isto está CAGADO!