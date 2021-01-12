import rle
import time
import numpy as np
import matplotlib.pyplot as plt

def entropy(prob: np.ndarray):
    """
    Função de cálculo da entropia de um ficheiro

    :param prob: Array com as probabilidades dos símbolos do ficheiro
    """
    non_zero = prob[prob > 0]
    return -np.sum(non_zero * np.log2(non_zero))

def hist(x_axis: np.ndarray, freq: np.ndarray, filename: str = None, x_start: float = None, x_end: float = None,
         x_label: str = None, y_label: str = None):
    """
    Função genérica de criação de histogramas

    :param x_axis: Array do eixo horizontal
    :param freq: Array do eixo vertical - frequências
    :param filename: Nome do ficheiro para o título do histograma
    :param x_start: Início do eixo horizontal (shift da janela)
    :param x_end: Fim do eixo horizontal (shift da janela)
    :param x_label: Nome do eixo horizontal
    :param y_label: Nome do eixo vertical
    """
    plt.figure("Histogram")

    if filename is not None and type(filename) == str:
        plt.title(f"Histogram of {filename}")
    else:
        plt.title("Histogram")

    if x_label is not None:
        plt.xlabel(x_label)
    else:
        plt.xlabel("Symbols")
    if y_label is not None:
        plt.ylabel(y_label)
    else:
        plt.ylabel("Absolute frequency")

    plt.bar(x_axis, freq, width=1, edgecolor="black", linewidth=0.4)

    if x_start is not None:
        plt.xlim(left=x_start)
    if x_end is not None:
        plt.xlim(right=x_end)

def show_img(data: np.ndarray, filename: str = None):
    """
    Mostra uma imagem com o Matplotlib

    :param data: Array resultante da função plt.imread
    :param filename: Nome do ficheiro para o título
    :return:
    """
    plt.figure("Image")
    plt.imshow(data)
    if filename is not None and type(filename) == str:
        plt.title(filename)
    plt.axis("off")

def is_img(filename: str, show_plots=True):
    """
    Função geral para abrir um ficheiro de imagem e chamar as funções auxiliares de cálculo

    :param filename: Nome do ficheiro de imagem
    :param show_plots: Criar histograma?
    """
    # Chamada das funções auxiliares de processamento e cálculo
    data = plt.imread(filename)
    x_axis, freq, size = process_img(data)
    h = entropy(freq / size)

    # Print file info
    print(f"Filename: {filename}\nEntropy = {h:.6f}")

    if show_plots:
        # Mostra a imagem e cria o histograma
        show_img(data, filename)
        hist(x_axis, freq, filename)
        plt.show()

def process_img(data: np.ndarray):
    """
    Função para processar imagens

    :param data: Array criado pela função plt.imread()
    """
    # Como as imagens serão monocromáticas, se existir canais RGB ou RGBA usar-se-á apenas um canal
    if data.ndim == 3:
        channel = data[:, :, 0]
    else:
        channel = data
    size = channel.size

    # Cálculo dos símbolos sem repetições e das frequências
    x_axis, freq = np.unique(channel, return_counts=True)

    return x_axis, freq, size

if __name__ == "__main__":
    is_img(r"data\original\egg.bmp")
    is_img(r"data\original\landscape.bmp")
    is_img(r"data\original\pattern.bmp")
    is_img(r"data\original\zebra.bmp")
