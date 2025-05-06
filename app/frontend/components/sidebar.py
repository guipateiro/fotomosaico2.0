##### ############# #####
### Quebra de arquivo ###
##### ############# #####

# Arquivo layout.py

import streamlit as st

# TABS ==================================================

def render_sidebar():
    # Botão para voltar à página inicial

    if st.sidebar.button(
        "Voltar para a Página Inicial",  # Texto do botão
        key="voltar_pagina_sla"  # Chave única
    ):
        st.switch_page("pages/initial_page.py")  # Altera para a página inicial

    # Botão para iniciar uma nova triagem
    if st.sidebar.button(
        '➕ NOVO FOTOMOSAICO',  # Texto exibido no botão
        key=f"nova_triagem_",  # Chave única com contexto
        use_container_width=True  # Faz o botão ocupar toda a largura da aba
    ):
        st.switch_page("pages/new_mosaic.py")

    if st.sidebar.button(
        '➕ NOVO CONJUNTO DE PASTILHAS',  # Texto exibido no botão
        key=f"nova_pastilha",  # Chave única com contexto
        use_container_width=True  # Faz o botão ocupar toda a largura da aba
    ):
        st.switch_page("pages/gerar_pastilha.py")

    if st.sidebar.button(
        '📁 CARREGAR PROJETO',  # Texto exibido no botão
        key=f"carregamento_triagem",  # Chave única com contexto
        use_container_width=True  # Faz o botão ocupar toda a largura da aba
    ):
        st.switch_page("pages/load_mosaic.py")

 
    

    