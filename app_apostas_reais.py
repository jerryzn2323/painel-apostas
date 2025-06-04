
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(layout="wide")
st.title("⚽ Painel de Apostas com Dados Reais - API-Football")

API_KEY = "adffc606910f25c06bcf7c0fef2d6140"
HEADERS = {
    "x-apisports-key": API_KEY
}

def buscar_jogos():
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "league": 71,
        "season": 2024
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        st.error("Erro ao buscar dados da API")
        return []

def analisar_jogo(jogo):
    try:
        time_casa = jogo['teams']['home']['name']
        time_fora = jogo['teams']['away']['name']
        status = jogo['fixture']['status']['long']
        st.subheader(f"{time_casa} x {time_fora}")
        st.write(f"Status: {status}")

        stats_home = jogo['teams']['home']['winner']
        stats_away = jogo['teams']['away']['winner']

        if stats_home is True:
            st.write("📌 Sugestão de aposta: ✅ Vitória do time da casa")
        elif stats_away is True:
            st.write("📌 Sugestão de aposta: ✅ Vitória do time visitante")
        else:
            st.write("⚠️ Sugestão: Dupla chance ou empate")
        st.markdown("---")
    except Exception as e:
        st.error(f"Erro ao analisar jogo: {e}")

jogos = buscar_jogos()

if jogos:
    for jogo in jogos:
        analisar_jogo(jogo)
else:
    st.info("Sem jogos disponíveis para análise hoje.")
