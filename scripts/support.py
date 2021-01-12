import sys
import numpy as np

# Move-to-Front Transform
def m2f_encode(data):
    order = list(range(256))
    size = len(data)    
    sequence = []
    for i in range(size):
        byte = data[i]
        index = order.index(byte)
        sequence.append(index)
        order = [order.pop(index)] + order

    return sequence

# Move-to-Front Reverse
def m2f_decode(data):
    order = list(range(0,256))
    sequence = []
    for index in data:
        byte = order[index]
        order = [order.pop(index)] + order
        sequence.append(byte)
    
    return sequence

# My own RLE reverser - the one provided by the module is most likely broken
def rle_decode(runs, lengths):
    if (len(runs) != len(lengths)):
        print("Invalid parameters", file=sys.stderr)
    
    sequence = []
    for i in range(len(runs)):
        for n in range(lengths[i]):
            sequence.append(runs[i])

    return sequence

# Delta Encoding
def delta_encode(data, times=1):
    for i in range(times):
        data = np.ediff1d(data, to_begin=data[0])
    return data

# Delta Decoder
def delta_decode(data):
    arr = np.cumsum(data)
    return np.mod(arr, 256)

# Entropy calculation
def entropy(prob: np.ndarray):
    """
    Função de cálculo da entropia de um ficheiro

    :param prob: Array com as probabilidades dos símbolos do ficheiro
    """
    non_zero = prob[prob > 0]
    return -np.sum(non_zero * np.log2(non_zero))