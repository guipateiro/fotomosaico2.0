import streamlit as st

import pytz
from components.sidebar import render_sidebar
from components.api import send_image

tz = pytz.timezone("America/Sao_Paulo")



# HEADER ==================================================
def render_header(title="placeholder"):
    """
    Renderiza o cabeçalho da página com o título fornecido.
    """
    st.header(title)
    st.markdown("---")

def new_mosaic():
    """
    Página de coleta de informações para triagem.
    Exibe os campos necessários e mantém a sidebar fixa.
    """
    # Renderiza o cabeçalho da página inicial
    render_header("O FOTOMOSAICO 2.0")
    render_sidebar()

    st.subheader("Coleta de Dados")

    # FORMULÁRIO DE TRIAGEM ==================================================
    def create_new_form():
        with st.form(key="triage_form", clear_on_submit=True):

            # Upload de imagem
            image = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg","webp"])

            # Parâmetros do formulário
            upscale = st.checkbox("Aumentar resolução (upscale)")
            solidTiles = st.checkbox("Usar ladrilhos sólidos (solidTiles)")
            generateMosaic = st.checkbox("Gerar mosaico (generateMosaic)")

            # Seleção da função desejada
            selectedFunction = st.selectbox(
                "Escolha a função",
                ["Função A", "Função B", "Função C"]
            )

            # Botão de submissão    
            finalizar = st.form_submit_button("Finalizar")

            # Se o botão for pressionado
            if finalizar:
                if image is not None:
                    # Criar um dicionário com os dados
                    files = {"image": image.getvalue()}
                    data = {
                        "upscale": upscale,
                        "solidTiles": solidTiles,
                        "generateMosaic": generateMosaic,
                        "selectedFunction": selectedFunction
                    }

                    # Enviar requisição para a API
                    response = send_image(files=files, data=data)

                    # Verificar resposta
                    if response.status_code == 200:
                        st.success("Dados enviados com sucesso!")
                    else:
                        st.error(f"Erro ao enviar os dados: {response.text}")
                else:
                    st.warning("Por favor, envie uma imagem antes de finalizar.")

    create_new_form()         

new_mosaic()
