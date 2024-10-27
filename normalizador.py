import os
import subprocess
import argparse
from PIL import Image

def resize_pastilhas(base_folder, new_size=32):
    # Criar a nova pasta para armazenar as imagens redimensionadas
    new_size=(new_size,new_size)
    new_folder = f"pastilhas_{new_size[0]}"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Percorrer todas as subpastas dentro da pasta principal
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.startswith("pastilha_") and file.endswith(".png"):
                # Caminho completo do arquivo
                file_path = os.path.join(root, file)
                
                # Abrir a imagem e redimensioná-la
                with Image.open(file_path) as img:
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Gerar um nome único para evitar sobreposição de arquivos
                    folder_name = os.path.basename(root)
                    base_name = os.path.splitext(file)[0]  # "pastilha_X"
                    new_file_name = f"{base_name}_{folder_name}.png"
                    
                    # Caminho completo para salvar a nova imagem
                    new_file_path = os.path.join(new_folder, new_file_name)
                    
                    # Salvar a imagem redimensionada
                    resized_img.save(new_file_path)

    print(f"Todas as pastilhas foram redimensionadas e salvas em '{new_folder}'.")

if __name__ == "__main__":
    # Configuração do argparse para lidar com argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Redimensionar pastilhas para um novo tamanho.")
    
    parser.add_argument("--folder", type=str, default="./pastilhas", help="Caminho para a pasta principal que contém as subpastas com pastilhas. Padrão ./pastilhas")
    parser.add_argument("--size", type=int, default=32, help="Novo tamanho das pastilhas (largura altura). Padrão 32.")
    
    args = parser.parse_args()
    
    # Executa a função de redimensionamento com os argumentos fornecidos
    resize_pastilhas(args.folder, args.size)

# Exemplo de uso:
# Base folder: a pasta principal que contém as subpastas
#base_folder = "."
#resize_pastilhas(base_folder)
#new_folder = f"pastilhas_{args.size}"
#subprocess.run(f"rm ./{new_folder}")
