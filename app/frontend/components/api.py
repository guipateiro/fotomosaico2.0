import requests
# Definição da URL da API
import streamlit as st
API_URL = "http://127.0.0.1:5000"  # Substitua pela URL real da sua API

def send_image(files,data):
    # Enviar requisição para a API
    response = requests.post(API_URL + '/iniciar', files=files, data=data)
    return response