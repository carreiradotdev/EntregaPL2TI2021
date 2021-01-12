import sys, os, lzma
import numpy as np
from time import time
    
def compress(data, savefile, preset=lzma.PRESET_DEFAULT):
    # Timing the full compression process
    init = time()
    
    original_size = len(data)

    # Delta Encode
    data = np.ediff1d(data, to_begin=data[0])
    print("Delta encoded")
    
    # Writing deltas as bytes
    encode = bytearray()
    for delta in np.nditer(data):
        encode.append(delta)
    encode = bytes(encode)

    # Compress bytes using LZMA
    compressed = lzma.compress(encode, preset=preset)
    print(f"Compressed using LZMA - Preset {preset} ")

    # Printing compression info
    print(f"Compression time: {(time() - init):.2f} s")
    compressed_size = len(compressed)
    print(f"Compression ratio: {original_size/compressed_size:.2f}")

    # Save compressed bytes to a binary file
    save(compressed, savepath)

def save(data, savepath):
    try: 
        with open(savepath, "wb") as f:
            f.write(data)
    except FileNotFoundError:
        print("This definitely should not have happened", file=sys.stderr)

def get_file(filepath):
    try:
        with open(filepath, "rb") as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        print(f"File does not exist: '{filepath}'", file=sys.stderr)
        exit(1)
    return data

if __name__ == "__main__":
    # Check for necessary command prompt arguments
    if len(sys.argv) < 2:
        print("Argument 1: file to compress", file=sys.stderr)
        print("Argument 2 (optional): compression level 0-9", file=sys.stderr)

        exit(2)
    
    # Parse arguments
    filepath = sys.argv[1]
    filename = filepath.split('\\')[-1].split('.')[0]
    savedir = fr"data\compressed\lzma"
    savepath = fr"{savedir}\{filename}"

    # Check if save directory exists, else create it
    if not os.access(savedir, os.F_OK):
        print("Creating save folder...")
        os.mkdir(savedir)

    if len(sys.argv) > 2:
        preset = int(sys.argv[2])
        compress(get_file(filepath), savepath, preset)
    else:
        compress(get_file(filepath), savepath)

    exit(0)