##### ############# #####
### Quebra de arquivo ###
##### ############# #####

# Arquivo page_3_triage_view.py

import streamlit as st
import numpy as np
import pytz
from components.sidebar import render_sidebar

fuso_horario = pytz.timezone("America/Sao_Paulo")  # Exemplo para o horário de Brasília

# HEADER ==================================================
def render_header(title="placeholder"):
    """
    Renderiza o cabeçalho da página com o título fornecido.
    """
    st.header(title)
    st.markdown("---")

# PÁGINA DE VISUALIZAÇÃO DE TRIAGEM ==================================================
def load_mosaic():
    """
    Página de visualização da triagem.
    Exibe os dados coletados e os resultados processados.
    """

    # Renderiza o cabeçalho da página inicial
    render_header("O FOTOMOSAICO 2.0")
    render_sidebar()

    selected_triage = st.session_state.get('selected_triage')

    # Verifica se há uma triagem selecionada
    if selected_triage >= 0:
        dados_triagem = None
        dados_triagem = dados_triagem[0]
        st.subheader("Dados da Triagem:")
        for key, value in dados_triagem.items():
            if key not in {"Data e Hora de Registro","Temperatura Corporal (°C)"}:
                st.markdown(f"- **{key}:** {value}")
            elif key in {"Data e Hora de Registro"}:
                st.markdown(f"- **{key}:** {value.astimezone(fuso_horario).strftime("%d/%m/%Y %H:%M:%S")}")
            elif key in {"Temperatura Corporal (°C)"}: 
                st.markdown(f"- **{key}:** {np.round(value,decimals=1)}")

load_mosaic()