import os
import numpy as np
from PIL import Image
from tqdm import tqdm  # Para mostrar progresso durante o processamento

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
caminho_imagem = "./fox.webp"
diretorio_pastilhas = "./pastilhas_32"
tamanho_bloco = (50, 50)  # Tamanho de cada pastilha/bloco em pixels

# Carregar imagem original e pastilhas
imagem_original = Image.open(caminho_imagem)
pastilhas = carregar_pastilhas(diretorio_pastilhas, tamanho_bloco)

# Criar fotomosaico
fotomosaico = criar_fotomosaico(imagem_original, pastilhas, tamanho_bloco)

# Salvar o resultado
fotomosaico.save("fotomosaico_final.jpg")
print("Fotomosaico criado e salvo como 'fotomosaico_final.jpg'.")
