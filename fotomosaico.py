import os
import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
from tqdm import tqdm  # Para mostrar progresso durante o processamento
import math
from pyciede2000 import ciede2000
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import tempfile
from collections import Counter
import re

def carregar_pastilhas(diretorio_pastilhas, tamanho_bloco):
    pastilhas = []
    nomes = []
    for nome_arquivo in os.listdir(diretorio_pastilhas):
        caminho = os.path.join(diretorio_pastilhas, nome_arquivo)
        try:
            imagem = Image.open(caminho).resize(tamanho_bloco)
            pastilhas.append(np.array(imagem))
            nomes.append(nome_arquivo)
        except:
            print(f"Erro ao abrir {caminho}. Ignorando.")
    return np.array(pastilhas), nomes

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
    largura, altura = imagem_original.size
    mosaico = Image.new('RGB', (largura, altura))
    cores_pastilhas = np.array([media_cor(p) for p in pastilhas])
    indices_usados = []

    for y in tqdm(range(0, altura, tamanho_bloco[1])):
        linha_indices = []
        for x in range(0, largura, tamanho_bloco[0]):
            bloco = imagem_original.crop((x, y, x + tamanho_bloco[0], y + tamanho_bloco[1]))
            cor_media_bloco = media_cor(np.array(bloco))
            indice_pastilha = encontrar_pastilha_mais_proxima(cor_media_bloco, cores_pastilhas)
            mosaico.paste(Image.fromarray(pastilhas[indice_pastilha]), (x, y))
            linha_indices.append(indice_pastilha)
        indices_usados.append(linha_indices)

    return mosaico, np.array(indices_usados).T  # Transpõe para [coluna][linha]

def criar_mosaico_com_grade(indices_por_linha, pastilhas, tamanho_bloco, espaco=2):
    linhas = len(indices_por_linha)
    colunas = len(indices_por_linha[0])
    largura_bloco, altura_bloco = tamanho_bloco

    largura_total = colunas * (largura_bloco + espaco) + espaco
    altura_total = linhas * (altura_bloco + espaco) + espaco

    imagem_com_grade = Image.new('RGB', (largura_total + 60, altura_total + 60), (255, 255, 255))
    draw = ImageDraw.Draw(imagem_com_grade)

    # Fonte para numeração (pode ajustar caminho ou usar padrão do sistema)
    try:
        fonte = ImageFont.truetype("arial.ttf", 14)
    except:
        fonte = ImageFont.load_default()

    for y, linha in enumerate(indices_por_linha):
        for x, idx in enumerate(linha):
            x_pos = x * (largura_bloco + espaco) + espaco + 60
            y_pos = y * (altura_bloco + espaco) + espaco + 20

            imagem_com_grade.paste(Image.fromarray(pastilhas[idx]), (x_pos, y_pos))

    # Desenhar linhas de grade
    for i in range(linhas + 1):
        y_line = i * (altura_bloco + espaco) + espaco + 20
        draw.line([(60, y_line), (largura_total + 60, y_line)], fill=(200, 200, 200), width=1)

    for j in range(colunas + 1):
        x_line = j * (largura_bloco + espaco) + espaco + 60
        draw.line([(x_line, 20), (x_line, altura_total + 20)], fill=(200, 200, 200), width=1)

    # Numeração
    for i in range(linhas):
        y_text = i * (altura_bloco + espaco) + espaco + 20 + altura_bloco // 2
        draw.text((5, y_text - 7), f"L{i+1}", font=fonte, fill=(0, 0, 0))

    for j in range(colunas):
        x_text = j * (largura_bloco + espaco) + espaco + 60 + largura_bloco // 2
        draw.text((x_text - 10, 5), f"C{j+1}", font=fonte, fill=(0, 0, 0))

    return imagem_com_grade


def gerar_pdf_colunas(indices_por_coluna, pastilhas, nomes_arquivos, tamanho_bloco, nome_pdf="mosaico_colunas.pdf"):
    largura_pagina, altura_pagina = A4
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    margem = 50
    linha_altura = 15

    # Contagem por nome completo da pastilha e por número do arquivo original (YYYY)
    padrao = re.compile(r"pastilha_\d+_CCI19052024_(\d+)\.png")
    contagem_pastilha = Counter()
    contagem_arquivo_original = Counter()

    for coluna in indices_por_coluna:
        for idx in coluna:
            nome = nomes_arquivos[idx]
            contagem_pastilha[nome] += 1
            match = padrao.match(nome)
            if match:
                y = match.group(1)
                contagem_arquivo_original[y] += 1

    # Escreve título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margem, altura_pagina - margem, "Resumo de Pastilhas Utilizadas")

    y_cursor = altura_pagina - margem - 25
    c.setFont("Helvetica", 12)
    c.drawString(margem, y_cursor, "Tabela 1 - Quantidade por nome da pastilha:")
    y_cursor -= linha_altura

    for nome, qtd in sorted(contagem_pastilha.items()):
        c.drawString(margem, y_cursor, f"{nome}: {qtd} vezes")
        y_cursor -= linha_altura
        if y_cursor < 100:
            c.showPage()
            y_cursor = altura_pagina - margem

    y_cursor -= 20
    c.setFont("Helvetica", 12)
    c.drawString(margem, y_cursor, "Tabela 2 - Quantidade por número do arquivo original (YYYY):")
    y_cursor -= linha_altura

    for y, qtd in sorted(contagem_arquivo_original.items(), key=lambda t: int(t[0])):
        c.drawString(margem, y_cursor, f"Arquivo {y}: {qtd} vezes")
        y_cursor -= linha_altura
        if y_cursor < 100:
            c.showPage()
            y_cursor = altura_pagina - margem

    c.showPage()
    max_por_pagina = int((altura_pagina - 2*margem) // (tamanho_bloco[1] + 10))

    for col_idx, coluna in enumerate(indices_por_coluna):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margem, altura_pagina - margem, f"Coluna {col_idx + 1}")
        y_cursor = altura_pagina - margem - 30
        count = 0
        for idx in coluna:
            nome_pastilha = nomes_arquivos[idx]
            imagem_pastilha = Image.fromarray(pastilhas[idx])
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                imagem_pastilha.save(tmp.name)
                img_reader = ImageReader(tmp.name)
                c.drawImage(img_reader, margem, y_cursor - tamanho_bloco[1], width=tamanho_bloco[0], height=tamanho_bloco[1])
            c.drawString(margem + tamanho_bloco[0] + 10, y_cursor - 5, nome_pastilha)
            y_cursor -= tamanho_bloco[1] + 10
            count += 1
            if count >= max_por_pagina:
                c.showPage()
                c.setFont("Helvetica-Bold", 14)
                y_cursor = altura_pagina - margem
                count = 0
        c.showPage()
    c.save()

# Caminhos e parâmetros
caminho_imagem = "./fox4.webp"
diretorio_pastilhas = "./pastilhas_32"
tamanho_bloco = (64, 64)  # Tamanho de cada pastilha/bloco em pixels

# Carregar imagem original e pastilhas
imagem_original = Image.open(caminho_imagem)
pastilhas, nomes_arquivos = carregar_pastilhas(diretorio_pastilhas, tamanho_bloco)

# Criar fotomosaico
fotomosaico = criar_fotomosaico(imagem_original, pastilhas, tamanho_bloco)

# Salvar o resultado
fotomosaico, indices_usados = criar_fotomosaico(imagem_original, pastilhas, tamanho_bloco)
fotomosaico.save("fotomosaico_final.jpg")
print("Fotomosaico criado e salvo como 'fotomosaico_final.jpg'.")

imagem_com_grade = criar_mosaico_com_grade(indices_usados.T, pastilhas, tamanho_bloco)
imagem_com_grade.save("fotomosaico_com_grade.jpg")
print("Imagem com grade e numeração salva.")

# Gerar PDF com colunas
gerar_pdf_colunas(indices_usados, pastilhas, nomes_arquivos, tamanho_bloco)
print("PDF gerado como 'mosaico_colunas.pdf'")
