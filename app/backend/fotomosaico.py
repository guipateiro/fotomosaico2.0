import os
import numpy as np
from PIL import Image
from tqdm import tqdm  # Para mostrar progresso durante o processamento
import math
from pyciede2000 import ciede2000

def carregar_pastilhas(diretorio_pastilhas, tamanho_bloco):
    """Carrega todas as pastilhas e as redimensiona para o tamanho do bloco."""
    pastilhas = []
    for nome_arquivo in os.listdir(diretorio_pastilhas):
        caminho = os.path.join(diretorio_pastilhas, nome_arquivo)
        try:
            imagem = Image.open(caminho).resize(tamanho_bloco)
            pastilhas.append(np.array(imagem))
        except:
            print(f"Erro ao abrir {caminho}. Ignorando.")
    return np.array(pastilhas)

def media_cor(imagem):
    """Calcula a cor média de uma imagem (R, G, B)."""
    return np.mean(imagem, axis=(0, 1))

def distanciacor(cor1, cor2):
    media_red = (cor1[0] + cor2[0]) / 2
    distancia = math.sqrt(
        ((2 + (media_red / 256)) * (cor1[0] - cor2[0]) ** 2) +
        (4 * (cor1[1] - cor2[1]) ** 2) +
        ((2 + (255 - media_red) / 256) * (cor1[2] - cor2[2]) ** 2)
    )
    return distancia

def rgb2lab ( inputColor ) :

   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )

   return Lab

'''
def encontrar_pastilha_mais_proxima(cor, cores_pastilhas):
    """Encontra o índice da pastilha cuja cor média é mais próxima da cor dada."""
    distancias = np.array([ciede2000(rgb2lab(cor),rgb2lab(cor_pastilha))['delta_E_00'] for cor_pastilha in cores_pastilhas])
    return np.argmin(distancias)
'''

def encontrar_pastilha_mais_proxima(cor, cores_pastilhas):
    """Encontra o índice da pastilha cuja cor média é mais próxima da cor dada."""
    distancias = np.sqrt(np.sum((cores_pastilhas - cor) ** 2, axis=1))
    return np.argmin(distancias)
def criar_fotomosaico(imagem_original, pastilhas, tamanho_bloco):
    """Cria um fotomosaico a partir da imagem original usando as pastilhas."""
    altura, largura = imagem_original.size
    mosaico = Image.new('RGB', (largura, altura))
    
    cores_pastilhas = np.array([media_cor(p) for p in pastilhas])
    
    for y in tqdm(range(0, altura, tamanho_bloco[1])):
        for x in range(0, largura, tamanho_bloco[0]):
            bloco = imagem_original.crop((x, y, x + tamanho_bloco[0], y + tamanho_bloco[1]))
            cor_media_bloco = media_cor(np.array(bloco))
            indice_pastilha = encontrar_pastilha_mais_proxima(cor_media_bloco, cores_pastilhas)
            mosaico.paste(Image.fromarray(pastilhas[indice_pastilha]), (x, y))

    return mosaico

# Caminhos e parâmetros
caminho_imagem = "./fox4.webp"
diretorio_pastilhas = "./pastilhas_32"
tamanho_bloco = (64, 64)  # Tamanho de cada pastilha/bloco em pixels

# Carregar imagem original e pastilhas
imagem_original = Image.open(caminho_imagem)
pastilhas = carregar_pastilhas(diretorio_pastilhas, tamanho_bloco)

# Criar fotomosaico
fotomosaico = criar_fotomosaico(imagem_original, pastilhas, tamanho_bloco)

# Salvar o resultado
fotomosaico.save("fotomosaico_final3.jpg")
print("Fotomosaico criado e salvo como 'fotomosaico_final.jpg'.")
