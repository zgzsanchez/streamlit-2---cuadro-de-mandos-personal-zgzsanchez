import requests
from pathlib import Path
import streamlit as st
import pandas as pd
import base64

# For more emojis code https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="NBA Stats", page_icon=":basketball:")


# displaying image function
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("NBA_header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)




st.title('Analizar estadísticas de jugadores de la NBA')

st.markdown("""
Datos obtenidos de: [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('Selecciona los años, equipos y posiciones para analizar')
selected_year = st.sidebar.selectbox('Años', list(reversed(range(1950,2022))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Equipos', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Posicion', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Datos de los jugadores con sus estadísticas')

st.dataframe(df_selected_team)

# Download NBA player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Descargar CSV</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)




