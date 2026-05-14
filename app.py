import streamlit as st
from src import api_client, storage

st.title("💊 CareTrack Web")
st.subheader("Assistente de Autocuidado para Idosos")

dica = api_client.get_daily_tip()
st.info(f"Dica do dia: {dica}")

dados = storage.load_data()
st.write("### Resumo de hoje")
st.write(f"💧 Água: {dados.get('agua_ml', 0)}ml")