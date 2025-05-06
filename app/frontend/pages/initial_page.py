import streamlit as st
from components.sidebar import render_sidebar

# HEADER ==================================================
def render_header_1(title="placeholder"):
    """
    Renderiza o cabeçalho da página com o título fornecido.
    """
    st.header(title)
    st.markdown("---")


# PÁGINA INICIAL ==================================================
def initial_page():
    render_header_1("🏥 O FOTOMOSAICO 2.0")
    render_sidebar()

    # Seção sobre o projeto
    st.subheader("Sobre o Projeto:")
    st.markdown(
            """texto inicial"""
        )

    col1, col2 = st.columns([3, 1])  # Cria duas colunas, maior espaço à esquerda
    with col2:  # Coloca o botão na coluna da direita
            if st.button("Iniciar projeto"):
                st.switch_page("pages/new_mosaic.py")
                
initial_page()