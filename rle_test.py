import sys, os, pickle
from scripts.support import rle_encode, rle_decode
import numpy as np
from time import time
    
def compress(data):
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

    runs, lengths = rle_encode(encode)

    compressed = pickle.dumps((runs,lengths))

    # Printing compression info
    print(f"Compression time: {(time() - init):.2f} s")
    compressed_size = len(compressed)
    print(f"Compression ratio: {original_size/compressed_size:.2f}")

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
        print("Script takes 1 argument - path to file to compress", file=sys.stderr)
        exit(2)
    
    # Parse arguments
    filepath = sys.argv[1]
    filename = filepath.split('\\')[-1].split('.')[0]

    compress(get_file(filepath))

    exit(0)