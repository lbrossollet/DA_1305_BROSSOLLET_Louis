import streamlit as st
import googlemaps
import gmaps
from datetime import datetime

# Définir votre clé API Google Maps
api_key = 'AIzaSyBND6dYdzOqlND5K-LQ2wJc0jBpUQIl2pQ'
gmaps_client = googlemaps.Client(key=api_key)

# Configurer gmaps avec votre clé API
gmaps.configure(api_key=api_key)

# Créer l'interface utilisateur avec Streamlit
st.title('Itinéraire sur une carte avec Google Maps et Streamlit')

# Entrée de l'utilisateur pour l'origine et la destination
origin = st.text_input('Origine', '')
destination = st.text_input('Destination', '')

# Bouton pour afficher l'itinéraire
if st.button('Afficher l\'itinéraire sur la carte'):
    try:
        # Obtenir les directions de l'API Google Maps
        directions_result = gmaps_client.directions(origin, destination, mode="driving", departure_time=datetime.now())

        # Récupérer les coordonnées des points de l'itinéraire
        coords = []
        for step in directions_result[0]['legs'][0]['steps']:
            start_loc = step['start_location']
            end_loc = step['end_location']
            coords.extend([(start_loc['lat'], start_loc['lng']), (end_loc['lat'], end_loc['lng'])])

        # Créer une carte centrée sur le premier point de l'itinéraire
        fig = gmaps.figure(center=coords[0], zoom_level=13, layout={'height': '600px', 'width': '800px'})


        # Ajouter la couche d'itinéraire à la carte
        itinerary_layer = gmaps.directions_layer(coords[0], coords[-1], waypoints=coords[1:-1])
        fig.add_layer(itinerary_layer)

        # Afficher la carte dans Streamlit
        st.write(fig)

    except Exception as e:
        st.error(f"Erreur lors de l'affichage de l'itinéraire : {e}")
