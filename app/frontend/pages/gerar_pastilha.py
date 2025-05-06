import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from components.sidebar import render_sidebar

# HEADER ==================================================
def render_header(title="🏥 Teste de Bancada EMERO PFS TOPSIS"):
    """
    Renderiza o cabeçalho da página com o título fornecido.
    """
    st.header(title)
    st.markdown("---")


# PÁGINA INICIAL ==================================================
def gerar_pastilha():
    render_header("🏥 O FOTOMOSAICO 2.0")
    render_sidebar()

    # Definição de variáveis globais
    if "clicks" not in st.session_state:
        st.session_state.clicks = []
    if "scale" not in st.session_state:
        st.session_state.scale = None
    if "confirmed" not in st.session_state:
        st.session_state.confirmed = False
    if "squares" not in st.session_state:
        st.session_state.squares = [(0,0,0)]
    if "reset" not in st.session_state:
        st.session_state.reset = True
    if "show" not in st.session_state:
        st.session_state.show = True
    if "square_pending_show" not in st.session_state:
        st.session_state.square_pending_show = False

    # Upload de imagem
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        width, height = image.size

        # Se a escala ainda não foi confirmada
        if not st.session_state.confirmed:

            st.write("### 1️⃣ Clique em dois pontos para definir a escala")
            if st.session_state.show:
                coords = streamlit_image_coordinates(image, key="scale_clicks")

                if coords and len(st.session_state.clicks) < 2 and not st.session_state.reset:
                    st.session_state.clicks.append((coords["x"], coords["y"]))
                st.session_state.reset = False

                # Se os dois pontos foram marcados, desenha a linha
                print(len(st.session_state.clicks))
                print(st.session_state.clicks)
            if len(st.session_state.clicks) == 2 and st.session_state.show == False:
                print("mostrando linha")
                x1, y1 = st.session_state.clicks[0]
                x2, y2 = st.session_state.clicks[1]

                # Criar imagem com linha
                image_with_line = image.copy()
                draw = ImageDraw.Draw(image_with_line)
                draw.line((x1, y1, x2, y2), fill="red", width=5)

                # Mostrar imagem com linha
                st.image(image_with_line, use_container_width=True)

                # Calcular a escala (supondo que a distância real entre os pontos é 3.5 cm)
                pixel_distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                st.session_state.scale = pixel_distance / 3.5
                st.write(f"**Escala calculada:** {st.session_state.scale:.2f} pixels/cm")

                # Botão para confirmar a escala
                if st.button("Confirmar Escala"):
                    st.session_state.confirmed = True
                    st.session_state.show = False 
                    st.session_state.reset = False
                    st.rerun()
                if st.button("Reiniciar Escala"):
                    st.session_state.clicks = [(0,0,0)]
                    st.session_state.reset = True
                    st.session_state.show = True
                    st.rerun()
            elif len(st.session_state.clicks) == 2:
                st.session_state.show = False
                print(len(st.session_state.clicks))
                print(st.session_state.clicks)
                print("not show")
                st.rerun()

        # Após confirmação, adicionar quadrados
        else:
            st.write("### 2️⃣ Clique na imagem para adicionar quadrados")
            print(st.session_state.squares)

            # Criar imagem com quadrados
            image_with_squares = image.copy()
            draw = ImageDraw.Draw(image_with_squares)

            # Se já houver quadrados, desenhá-los
            for x, y, size in st.session_state.squares:
                draw.rectangle([x - size/2, y - size/2, x + size/2, y + size/2], outline="blue", width=2)

            coords = None
            # Mostrar imagem para adicionar quadrados
            print(st.session_state.reset)
            print(st.session_state.confirmed)
            if not st.session_state.reset:
                coords = streamlit_image_coordinates(image_with_squares, key="square_clicks")
            st.session_state.reset = False
            print(coords)
            
            if coords and st.session_state.square_pending_show == False and (coords["x"] != st.session_state.squares[-1][0] or coords["y"] != st.session_state.squares[-1][1]):
                st.session_state.square_pending_show = True
                x, y = coords["x"], coords["y"]
                square_size = st.session_state.scale * 0.5  # 0.5 cm convertido para pixels
                st.session_state.squares.append((x, y, square_size))
                print("adicionado quadrado")
                st.rerun()
            elif st.session_state.square_pending_show == True:
                st.session_state.square_pending_show = False

            # Exibir tabela com quadrados adicionados
            if len(st.session_state.squares) > 10 :
                df = pd.DataFrame(st.session_state.squares[-19:], columns=["X", "Y", "Tamanho (px)"])
                st.dataframe(df)
            elif len(st.session_state.squares) > 1:
                df = pd.DataFrame(st.session_state.squares[1:], columns=["X", "Y", "Tamanho (px)"])
                st.dataframe(df)

            # Botão para resetar quadrados
            if st.button("Resetar Quadrados"):
                print("reset")
                st.session_state.squares = [(0,0,0)]
                st.session_state.reset = True
                st.session_state.confirmed = False
                st.rerun()
            if st.button("Enviar pastilhas"):
                
                st.rerun()

gerar_pastilha()