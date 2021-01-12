import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from huffmancodec import HuffmanCodec


# --------------------- PLOTTING AND INFO PRINT ---------------------

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


def print_info(filename: str, size: int, entropy_value: float, codes_len: float = None, codes_var: float = None,
               grouped: float = None):
    """
    Função de output de informação de ficheiros

    :param filename: Nome do ficheiro
    :param size: Tamanho do ficheiro (número total de símbolos)
    :param entropy_value: Entropia do ficheiro
    :param codes_len: Tamanho médio dos comprimentos dos códigos de Huffman
    :param codes_var: Variância dos tamanhos dos códigos de Huffman
    :param grouped: Entropia do ficheiro após o agrupamento de símbolos contíguos
    """
    print(f"File: {filename}")
    print(f"Size of information source: {size}")
    print(f"Calculated entropy: {entropy_value:.6f}")
    if grouped is not None:
        print(f"Pairing entropy: {grouped:.6f}")
    if codes_len is not None:
        print(f"Huffman codes mean length: {codes_len:.6f}")
    if codes_var is not None:
        print(f"Huffman codes variance: {codes_var:.6f}")
    print("")


# --------------------- DATA TREATMENT ---------------------

def entropy(prob: np.ndarray):
    """
    Função de cálculo da entropia de um ficheiro

    :param prob: Array com as probabilidades dos símbolos do ficheiro
    """
    non_zero = prob[prob > 0]
    return -np.sum(non_zero * np.log2(non_zero))


def huff(data: np.ndarray, prob: np.ndarray, show_plot: bool = False):
    """
    Função de cálculo do comprimento médio e variação dos comprimentos dos códigos de Huffman

    :param data: Array com os símbolos do ficheiro
    :param prob:  Array com as probabilidades de ocorrência dos símbolos do ficheiro
    :param show_plot: Criar o gráfico do tamanho do código de Huffman por símbolo?
    """
    # Recurso aos algoritmo fornecido pelo professor
    codec = HuffmanCodec.from_data(data.flatten())
    if show_plot:
        symbols, lengths = codec.get_code_len()
        symbols = np.asarray(symbols)
        lengths = np.asarray(lengths)
        plt.figure("Huffman Codes Lengths")
        plt.title("Huffman Codes Lengths")
        plt.xlabel("Symbol")
        plt.ylabel("Code Length")
        plt.bar(symbols, lengths, edgecolor="black", linewidth=0.4)
        plt.show()
    else:
        lengths = np.asarray(codec.get_code_len()[1])

    if lengths.size != prob.size:
        prob = prob[prob > 0]

    # Comprimento médio dos códigos de Huffman
    mean_len = sum(prob * lengths)
    # Variância dos comprimentos de Huffman
    var = np.average((lengths - mean_len) ** 2, weights=prob)

    return mean_len, var


def group_two(data: np.ndarray):
    """
    Função de agrupamento de símbolos contíguos e cálculo de entropia por símbolo simples

    :param data:
    """
    # Caso o tamanho seja par, podemos usar todos os símbolos para criar pares
    # Senão, remove-se o último símbolo para agrupar os restantes
    if data.size % 2 == 0:
        new_size = int(data.size / 2)
        grouped = data.reshape(new_size, 2)
    else:
        new_size = int((data.size - 1) / 2)
        grouped = data[:-1].reshape(new_size, 2)

    # Array que vai conter um versão simplificada do agrupamento
    simple = np.empty(new_size)

    # O novo símbolo vai ser calculado: 1º símbolo * tamanho da fonte + 2º símbolo
    for i in np.arange(new_size):
        simple[i] = grouped[i][0] * data.size + grouped[i][1]

    # Cálculo das frequências dos símbolos agrupados
    simple_freq = np.unique(simple, return_counts=True)[1]

    # Como a entropia é o número de bits para 2 símbolos, retornar metade da entropia
    return entropy(simple_freq / new_size) / 2


def is_text(filename: str, show_plots=True):
    """
    Função geral para abrir um ficheiro de texto e chamar as funções auxiliares de cálculo

    :param filename: Nome do ficheiro de texto
    :param show_plots: Criar histograma?
    """
    # Abrir o texto para uma string
    with open(filename, 'r')as f:
        text = f.read()
        f.close()

    # Chamada das funções auxiliares de processamento e cálculo
    x_axis, freq, ascii_codes, size = process_text(text)
    h = entropy(freq / size)
    codes_len, codes_var = huff(ascii_codes, freq / size, show_plot=True)
    group_entropy = group_two(ascii_codes)

    # Output da informação calculada
    print_info(filename, size, h, codes_len, codes_var, group_entropy)

    if show_plots:
        # Cria o histograma
        hist(x_axis, freq, filename)

        # Mostra o histograma
        plt.show()


def process_text(text: str):
    """
    Função para processar o texto

    :param text: String com o ficheiro de texto lido
    """
    # Converter texto para array de códigos ASCII (char pertencente a A-Za-z)
    ascii_codes = []
    for char in text:
        code = ord(char)
        if 64 < code < 91 or 96 < code < 123:
            ascii_codes.append(ord(char))

    ascii_codes = np.asarray(ascii_codes)
    size = ascii_codes.size

    # Cria o array com A-Za-z para o eixo horizontal do histograma
    x_axis = np.empty(52, dtype=np.str_)
    for i in np.arange(52):
        if i < 26:
            x_axis[i] = chr(i + 65)
        else:
            x_axis[i] = chr(i + 71)

    # Cálculo iterativo das frequências para cada char
    freq = np.zeros(52, dtype=np.int64)
    for code in ascii_codes:
        if 64 < code < 91:
            freq[code - 65] += 1
        elif 96 < code < 123:
            freq[code - 71] += 1

    return x_axis, freq, ascii_codes, size


def is_img(filename: str, show_plots=True):
    """
    Função geral para abrir um ficheiro de imagem e chamar as funções auxiliares de cálculo

    :param filename: Nome do ficheiro de imagem
    :param show_plots: Criar histograma?
    """
    # Chamada das funções auxiliares de processamento e cálculo
    data = plt.imread(filename)
    x_axis, freq, size, codes_len, codes_var = process_img(data)
    h = entropy(freq / size)
    if data.ndim == 3:
        group_entropy = group_two(data[:, :, 0])
    else:
        group_entropy = group_two(data)

    # Output da informação calculada
    print_info(filename, size, h, codes_len, codes_var, group_entropy)

    if show_plots:
        # Mostra a imagem e cria o histograma
        show_img(data, filename)
        hist(x_axis, freq, filename, x_axis[0] - 5)
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

    # Cálculo de comprimento médio e variância dos códigos de Huffman
    codes_len, codes_var = huff(channel.flatten(), freq / size, show_plot=True)

    return x_axis, freq, size, codes_len, codes_var


def is_wav(filename: str, show_plots=True):
    """
    Função geral para abrir um ficheiro de som e chamar as funções auxiliares de cálculo

    :param filename: Nome do ficheiro de som
    :param show_plots: Criar histograma?
    """
    data = wavfile.read(filename)[1]  # Ignora o sample rate, inútil para a entropia

    # Chamada das funções auxiliares de processamento e cálculo
    symbols, freq, size, codes_len, codes_var = process_wav(data)
    h = entropy(freq / size)
    if data.ndim == 2:
        group_entropy = group_two(data[:, 0])
    else:
        group_entropy = group_two(data)

    # Output da informação calculada
    print_info(filename, size, h, codes_len, codes_var, group_entropy)

    if show_plots:
        # Cria o histograma
        hist(symbols, freq, filename, symbols[0] - 5)
        plt.show()


def process_wav(data: np.ndarray):
    """
    Função para processar som

    :param data: Array criado pela função scipy.io.wavfile.read()
    """
    # Se o aúdio for stereo, usar apenas o canal esquerdo
    if data.ndim == 2:
        channel = data[:, 0]
    else:
        channel = data
    size = channel.size

    # Cálculo dos símbolos sem repetições e das frequências
    symbols, freq = np.unique(channel, return_counts=True)

    # Cálculo de comprimento médio e variância dos códigos de Huffman
    codes_len, codes_var = huff(channel, freq / size, show_plot=True)

    return symbols, freq, size, codes_len, codes_var


# --------------------- MUTUAL INFORMATION ---------------------

def get_frames(query: np.ndarray, target: np.ndarray, step: int):
    """
    Função para criação das janelas do target

    :param query: Sinal a pesquisar
    :param target: Sinal onde pesquisar (alvo)
    :param step: Intervalo entre janelas
    """
    # Cria o array com os índices de ínicio das janelas
    indices = np.arange(0, target.size - query.size + 1, step)

    # Cria o array para armazenar as janelas
    frames = np.empty(indices.size, dtype=np.ndarray)
    
    # Calcula e armazena as janelas 
    j = 0
    for i in indices:
        frames[j] = target[i:i + query.size]
        j += 1
    return frames


def mutual_info(x: np.ndarray, y: np.ndarray, symbols: np.ndarray):
    """
    Função de cálculo da probabilidade conjunta - P(x,y)

    :param x: Fonte de informação
    :param y: Fonte de informação
    :param symbols: Array do alfabeto das fontes
    """
    # Probabilidade conjunta
    both_freq = np.zeros((symbols.size, symbols.size))
    # Assumimos que x e y têm o mesmo tamanho
    for i in range(x.size):
        both_freq[x[i] - symbols[0], y[i] - symbols[0]] += 1
    both_prob = both_freq / np.sum(both_freq)

    # Frequências de x, incluindo freq = 0
    x_freq = np.zeros(symbols.size)
    for x_i in np.nditer(x):
        x_freq[x_i - symbols[0]] += 1
    x_prob = x_freq / x.size

    # Frequências de y, incluindo freq = 0
    y_freq = np.zeros(symbols.size)
    for y_i in np.nditer(y):
        y_freq[y_i - symbols[0]] += 1
    y_prob = y_freq / y.size

    # Calculo da informação mútua usando a distância de Kullback-Leibler de P(X,Y) e P(X)P(Y)
    h = 0
    for i in range(symbols.size):
        for j in range(symbols.size):
            if both_prob[i, j] > 0 and x_prob[i] > 0 and y_prob[j] > 0:
                log = both_prob[i, j] / (x_prob[i] * y_prob[j])
                h += both_prob[i, j] * np.log2(log)
    return h


def window_mutual(query: np.ndarray, target: np.ndarray, step: int):
    """
    Função com us das janelas para cálculo da informação mútua em cada janela do alvo

    :param query: Array do wavfile.read() da query
    :param target: Array do wavfile.read() do alvo
    :param step: Interval between windows
    """
    # Cria o array com as janelas
    frames = get_frames(query, target, step)

    # Cria o alfabeto usando os extremos da união das duas fontes
    symbols_min = min(np.min(query), np.min(target))
    symbols_max = max(np.max(query), np.max(target))
    symbols = np.arange(symbols_min, symbols_max + 1)

    # Cria o array com os valores de informação mútua para cada janela
    mutual_information = np.zeros(frames.shape[0])
    for i in range(mutual_information.size):
        mutual_information[i] = mutual_info(query, frames[i], symbols)

    return mutual_information


def run_mutual(query_filename: str, target_filename: str, step: int = None, show_plots=False):
    """
    Função de cálculo da informação mútua entre a query e o alvo, com janelas intervaladas

    :param query_filename: Nome do ficheiro query
    :param target_filename: Nome do ficheiro alvo
    :param step: Tamanho do intervalo entre janelas do alvo
    :param show_plots: Criar o gráfico da informação mútua por janela do alvo?
    """
    query = wavfile.read(query_filename)[1]
    target = wavfile.read(target_filename)[1]

    # Se o ficheiro for stereo, isolar o canal esquerdo 
    if query.ndim == 2:
        query = query[:, 0]
    if target.ndim == 2:
        target = target[:, 0]

    # Se o step não for especificado, usar um default
    if step is None:
        step = int(query.size / 4)

    # Imprimir o array de informação mútua com 4 casas decimais
    with np.printoptions(precision=4):
        print(f"Average mutual information for \"{target_filename}\" and \"{query_filename}\", in frames:")
        windows = window_mutual(query, target, step)
        print(f"\t{windows}")

    # Se show_plots == True, mostrar o gráfico da informação mútua em cada janela
    if show_plots:
        plt.figure("Average mutual information")
        plt.ylabel("Average mutual information")
        plt.xlabel("Frame")
        plt.title(f"{query_filename} e {target_filename}")
        plt.bar(np.arange(1, windows.size + 1), windows, width=0.9, edgecolor="black", linewidth=0.4)
        plt.xticks(np.arange(1, windows.size + 1))
        plt.show()


def shazam(query_filename: str):
    """
    Função de comparação de uma query (audio file) aos alvos "Song*.wav"

    :param query_filename: Nome do ficheiro da query
    """
    query = wavfile.read(query_filename)[1]
    
    # Se o ficheiro for stereo, isolar o canal esquerdo
    if query.ndim == 2:
        query = query[:, 0]

    # Intervalo fixo, dado no enunciado
    step = int(query.size / 4)

    # Cria uma lista de targets para iterar mais tarde
    targets = []
    for i in range(1, 8):
        targets.append(rf"data\Song0{i}.wav")

    # Cria o array para armazenar (info_mutua_maxima, target_index)
    maxes = np.empty(7, dtype=tuple)

    # Calcular a informação mútua em janelas, determinar a máxima e armazenar (info_mutua_maxima, target_index)
    for i in range(7):
        print(f"Average mutual information for \"{query_filename}\" and \"{targets[i]}\":")
        target = wavfile.read(targets[i])[1]
        if target.ndim == 2:
            target = target[:, 0]
        mutual_info = window_mutual(query, target, step)
        print(f"\t{mutual_info}")
        maxes[i] = np.max(mutual_info), i

    # Sort descendente de maxes
    maxes = np.flip(np.sort(maxes))

    # Print dos resultados do sort
    print("\nSearch results, from best fit to worst:")
    for info, index in maxes:
        print(f"\t{targets[index]} with mutual info: {info:.4f}")


if __name__ == "__main__":
    #  -------------------- Ex 1 - 5: Histogramas, entropias e códigos de Huffman --------------------
    is_img(r"data\lena.bmp", show_plots=False)
    is_img(r"data\ct1.bmp", show_plots=False)
    is_img(r"data\binaria.bmp", show_plots=False)
    is_wav(r"data\saxriff.wav", show_plots=False)
    is_text(r"data\texto.txt", show_plots=False)

    #  -------------------- Ex 6: Informação mútua --------------------
    # query_filename = r"data\saxriff.wav"
    # run_mutual(query_filename, r"data\target01 - repeat.wav", show_plots=True)
    # run_mutual(query_filename, r"data\target02 - repeatNoise.wav", show_plots=True)
    # shazam(query_filename)
