import streamlit as st
import requests
import folium

# Définition de l'URL de l'API Flask
API_URL = 'http://localhost:8080'

# Fonction pour récupérer les données depuis l'API
def fetch_data(endpoint):
    response = requests.get(API_URL + endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error fetching data: {response.status_code}')

# Configuration de l'application Streamlit
def main():
    st.title('Traffic Data Dashboard')

    # Exemple d'appel à l'API pour récupérer les données de traffic
    st.header('Traffic Data')
    traffic_data = fetch_data('traffic')
    if traffic_data:
        st.write(traffic_data)

    # Exemple d'appel à l'API pour afficher une carte avec Folium
    st.header('Map')
    map_html = fetch_data('map')
    if map_html:
        st.markdown(map_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
