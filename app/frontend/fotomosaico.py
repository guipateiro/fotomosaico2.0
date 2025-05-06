##### ############# #####
### Quebra de arquivo ###
##### ############# #####

# Arquivo emero.py

import streamlit as st
#from frontend.new_mosaic import new_mosaic
#from frontend.load_mosaic import load_mosaic
#from frontend.initial_page import initial_page
from components.sidebar import render_sidebar


# Configurações gerais da aplicação
st.set_page_config(page_title="initial", layout="wide")

# Inicialização do estado da sessão
if 'page' not in st.session_state:
    st.session_state['page'] = 'page'

# Função principal
def main():
    # Inicializa o estado da sessão
    render_sidebar()
    # Controle de navegação entre as páginas
    st.switch_page("pages/initial_page.py")
    print('loop')

# Garantia de execução
if __name__ == "__main__":
    main()
    
    
   
   
                 