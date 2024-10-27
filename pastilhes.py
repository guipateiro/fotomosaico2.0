import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Carregar a imagem
image_path = 'CCI19052024_0012.jpg'
image = Image.open(image_path)

# Função para desenhar a linha de referência
def onclick(event):
    global line_points
    if len(line_points) < 2:
        line_points.append((event.xdata, event.ydata))
        if len(line_points) == 2:
            ax.plot([line_points[0][0], line_points[1][0]], 
                    [line_points[0][1], line_points[1][1]], 
                    color='red')
            fig.canvas.draw()
            calculate_scale()

# Função para calcular a escala
def calculate_scale():
    global scale
    dx = line_points[1][0] - line_points[0][0]
    dy = line_points[1][1] - line_points[0][1]
    pixel_distance = (dx**2 + dy**2)**0.5
    scale = pixel_distance / 3.5  # pixels por centímetro

# Função para desenhar quadrados de 0,5 cm
def draw_square(event):
    global squares
    if scale:
        square_size = 0.5 * scale  # tamanho do quadrado em pixels
        x, y = event.xdata, event.ydata
        rect = plt.Rectangle((x - square_size/2, y - square_size/2), 
                             square_size, square_size, 
                             linewidth=1, edgecolor='blue', facecolor='none')
        ax.add_patch(rect)
        
        # Adicionar o número dentro do quadrado
        num = len(squares) + 1
        ax.text(x, y, str(num), color='blue', ha='center', va='center')
        
        fig.canvas.draw()
        squares.append((x, y, square_size, num))
        save_square(x, y, square_size, num)

# Função para salvar os quadrados
def save_square(x, y, square_size, num):
    # Cria a pasta 'pastilhas' se não existir
    if not os.path.exists(f'pastilhas/{image_path.split('.')[0]}/'):
        os.makedirs(f'pastilhas/{image_path.split('.')[0]}/')
    
    # Recorta o quadrado da imagem
    left = int(x - square_size/2)
    upper = int(y - square_size/2)
    right = int(x + square_size/2)
    lower = int(y + square_size/2)
    
    square_image = image.crop((left, upper, right, lower))
    
    # Nomeia e salva o quadrado
    square_filename = f'pastilhas/{image_path.split('.')[0]}/pastilha_{num}.png'
    square_image.save(square_filename)

def save_final_image():
    # Desenhar na imagem original
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    for (x, y, square_size, num) in squares:
        left = int(x - square_size/2)
        upper = int(y - square_size/2)
        right = int(x + square_size/2)
        lower = int(y + square_size/2)
        
        # Desenha o retângulo
        draw.rectangle([left, upper, right, lower], outline="blue")
        
        # Adiciona o número
        text_x = x - square_size/4  # Centraliza o texto no quadrado
        text_y = y - square_size/4
        draw.text((text_x, text_y), str(num), fill="blue", font=font)
    
    # Salva a imagem final
    image.save(f'pastilhas/{image_path.split('.')[0]}/final_image.png')

# Configurar a exibição da imagem e a interação
fig, ax = plt.subplots()
ax.imshow(image)
line_points = []
squares = []
scale = None

# Conectar os eventos
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_press_event', draw_square)

plt.show()

save_final_image()