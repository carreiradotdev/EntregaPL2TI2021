import sys, os, bz2
import numpy as np
from time import time
    
def compress(data, savepath, cl=9):
    # Timing the full compression process
    init = time()
    
    # Original size of data in bytes
    original_size = len(data)

    # Delta encoding of data
    data = np.ediff1d(data, to_begin=data[0])
    
    # Compress delta encoded data using BZip2 with a compression level cl
    compressed_data = bz2.compress(data, cl)

    # Final size after Delta Encoding + BZip2 in bytes
    compressed_size = len(compressed_data)

    # Printing compression info
    elapsed = time() - init
    ratio = original_size/compressed_size
    print(f"Compression time: {elapsed:.2f} s")
    print(f"Compression ratio: {ratio:.2f}")
    
    # save(compressed_data, savepath)

def get_file(filepath):
    try:
        with open(filepath, "rb") as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        print(f"File does not exist: '{filepath}'", file=sys.stderr)
        exit(1)
    return data

def save(data, savepath):
    try: 
        with open(savepath, "wb") as f:
            f.write(data)
    except FileNotFoundError:
        print("This definitely should not have happened", file=sys.stderr)
        
if __name__ == "__main__":
    # Check for necessary command prompt arguments
    if len(sys.argv) < 2:
        print("Missing arguments", file=sys.stderr)
        exit(2)
    
    # Parse arguments
    filepath = sys.argv[1]
    filename = filepath.split('\\')[-1].split('.')[0]
    cl = int(sys.argv[2])
    savedir = fr"data\compressed\bz2\cl{cl}"
    savepath = fr"{savedir}\{filename}"
    
    # Check if save directory exists, else create it
    if not os.access(savedir, os.F_OK):
        os.mkdir(fr"compressed\bz2\cl{cl}")

    if len(sys.argv) > 2:
        compress(get_file(filepath), savepath, cl)
    else:
        compress(get_file(filepath), savepath)
    
    exit(0)