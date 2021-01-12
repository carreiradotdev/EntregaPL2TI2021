# Resumos de codecs lossless de imagem
* * *
## Burrow-Wheeler Transform
De uma sequência de tamanho n, criar n-1 shifts cíclicos, ordenar lexicograficamente e armazenar a última coluna (últimos símbolos de cada linha).
* * *
## Move to Front
Geralmente precedido por BWT.


* * *
## JPEG Lossless - 1993
Adição ao standard lossy JPEG para a compressão não-destrutiva de imagens.

Faz uso de 7 esquemas preditivos (necessário a escolha do esquema), ou codificação sem esquema preditivo.

    1 - Î(i,j) = I(i-1,j)
    2 - Î(i,j) = I(i,j-1)
    3 - Î(i,j) = I(i-1,j-1)
    4 - Î(i,j) = I(i,j-1) + I(i-1,j) - I(i-1,j-1)
    5 - Î(i,j) = I(i,j-1) + (I(i-1,j) - I(i-1,j-1))/2
    6 - Î(i,j) = I(i-1,j) + (I(i,j-1) - I(i-1,j-1))/2
    7 - Î(i,j) = (I(i,j-1) + I(i-1,j))/2

As diferenças entre os valores reais e previstos (resíduo) é então codificado com um algoritmo entrópico (Huffman ou Aritmético)

O JPEG Lossless ainda é usado por exemplo, para imagens médicas.

Para determinar a melhor compressão seria preciso comprimir com os 8 esquemas e escolher o melhor resultado.
* * *
## FELICS (Fast, Efficient & Lossless Image Compression System)
O algoritmo é cerca de 5x mais rápido que o JPEG lossless mode ('93), mas com uma compressão equiparável
* * *
## CALIC (Context Adaptive Lossless Image Compression)
Funciona em 2 modos: i) grayscale, e ii) bi-level (binária).

Faz uso de que numa imagem, um pixel geralmente tem um valor semelhante a um dos seus vizinhos. Qual dos vizinhos dará uma previsão mais precisa depende da estrutura da imagem.

O algoritmo determina a estrutura local para o pixel a ser codificado de forma adaptativa, e pode até alterar de modo on-the-fly e de forma transparente.
* * *
## LOCO-I (JPEG-LS)
Assemelha-se a CALIC, mas usa um codificador preditivo de menor complexidade com performance semelhante.
* * * 
## PNG (Portable Network Graphics)
https://www.w3.org/TR/PNG/#9Filters


https://en.wikipedia.org/wiki/Portable_Network_Graphics

Sayood Edição 5

Surgiu como resposta a patenteação do GIF.

Pré compressão é escolhido um método de filtragem para o ficheiro, embora só exista um método na especificação internacional, e um um tipo de filtro para prever cada byte:
   
    0: X
    1: X - A
    2: X - B
    3: X - (A + B) // 2
    4: X - Paeth(A,B,C)

    Diagrama de bytes:
    C   B
    A   X

Paeth:

    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc then Pr = a
    else if pb <= pc then Pr = b
    else Pr = c
    return Pr

O algoritmo escolhe um tipo de filtro para cada linha de forma a melhorar a previsão e, consequentemente, a compressão.
O erro de previsão é então comprimido usando Deflate.
* * *
## Conclusão
Muitos dos algoritmos vistos tentam primero descorrelacionar os dados usando transformadas ou previsão de dados de forma a baixar a entropia, sendo assim possível uma maior compressão usando codificadores entrópicos.    