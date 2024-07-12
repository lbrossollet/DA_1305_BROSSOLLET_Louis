import streamlit as st
import googlemaps
import folium
from streamlit_folium import st_folium

# Définir votre clé API Google Maps
api_key = 'AIzaSyBND6dYdzOqlND5K-LQ2wJc0jBpUQIl2pQ'  # Remplacez 'YOUR_API_KEY' par votre clé API réelle
gmaps = googlemaps.Client(key=api_key)

# Créer l'interface utilisateur avec Streamlit
st.title('API Google Maps Directions avec Streamlit et Folium')

# Entrée de l'utilisateur pour l'origine et la destination
origin = st.text_input('Origine', 'Châtelet, Paris')
destination = st.text_input('Destination', 'Tour Eiffel, Paris')

# Bouton pour obtenir les directions
if st.button('Obtenir les directions'):
    # Faire une requête à l'API Directions
    try:
        directions_result = gmaps.directions(origin, destination, mode="driving")
        steps = directions_result[0]['legs'][0]['steps']

        # Afficher les étapes de l'itinéraire
        st.subheader('Étapes de l\'itinéraire:')
        for step in steps:
            st.markdown(f"{step['html_instructions']} - {step['distance']['text']}, {step['duration']['text']}")

        # Récupérer toutes les coordonnées de l'itinéraire
        path_coords = []
        for step in steps:
            polyline = step['polyline']['points']
            decoded_points = googlemaps.convert.decode_polyline(polyline)
            path_coords.extend(decoded_points)

        # Créer une carte Folium centrée sur l'origine
        map_center = path_coords[0]
        folium_map = folium.Map(location=[map_center['lat'], map_center['lng']], zoom_start=13)

        # Ajouter l'itinéraire à la carte Folium
        folium.PolyLine([(point['lat'], point['lng']) for point in path_coords], color="blue", weight=2.5, opacity=1).add_to(folium_map)

        # Afficher la carte Folium dans Streamlit
        st_folium(folium_map, width=800, height=600)

    except Exception as e:
        st.error(f"Erreur lors de l'obtention des directions: {e}")
