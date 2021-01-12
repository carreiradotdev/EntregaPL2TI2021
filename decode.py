import sys, os, lzma
import numpy as np
from time import time

def decompress(data, savefile):
    # Timing the full decompression process
    init = time()

    # Decompress bytes using LZMA
    data = lzma.decompress(data)
    
    # Restore original bytes from delta encoding
    revert = bytearray(data)
    revert = np.cumsum(revert)
    revert = np.mod(revert, 256)
    
    # Convert np.ndarray to bytes
    final = bytearray()
    for byte in revert:
        final.append(byte)
    final = bytes(final)

    # Printing decompression info
    print(f"Decompression time: {time()-init:.2f} s")

    # Save decompressed bytes back to a bitmap file
    save(final, savepath)

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
    if len(sys.argv) != 2:
        print("Argument 1: file to decompress", file=sys.stderr)
        exit(2)

    # Parse arguments
    filepath = sys.argv[1]
    filename = sys.argv[1].split('\\')[-1].split('.')[0]
    savedir = "data\decompressed"
    savepath = fr"{savedir}\{filename}.bmp"

    # Check if save directory exists, else create it
    if not os.access(savedir, os.F_OK):
        print("Creating save folder...")
        os.mkdir(savedir)

    decompress(get_file(filepath), savepath)

    exit(0)