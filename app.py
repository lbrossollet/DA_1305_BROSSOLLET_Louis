import streamlit as st
import googlemaps
import json

# Définir votre clé API Google Maps
api_key = 'AIzaSyBND6dYdzOqlND5K-LQ2wJc0jBpUQIl2pQ'  # Remplacez 'YOUR_API_KEY' par votre clé API réelle
gmaps = googlemaps.Client(key=api_key)

# Créer l'interface utilisateur avec Streamlit
st.title('API Google Maps Directions avec Streamlit')

# Entrée de l'utilisateur pour l'origine et la destination
origin = st.text_input('Origine', 'place_id:ChIJN1t_tDeuEmsRUsoyG83frY4')
destination = st.text_input('Destination', 'place_id:ChIJK_79wNWuEmsR3KHAgiEksm4')

# Bouton pour obtenir les directions
if st.button('Obtenir les directions'):
    # Faire une requête à l'API Directions
    try:
        directions_result = gmaps.directions(origin, destination)
        steps = directions_result[0]['legs'][0]['steps']

        # Afficher les étapes de l'itinéraire
        st.subheader('Étapes de l\'itinéraire:')
        for step in steps:
            st.markdown(f"{step['html_instructions']} - {step['distance']['text']}, {step['duration']['text']}")

        # Afficher le JSON complet pour plus de détails
        st.subheader('Détails complets de la réponse de l\'API:')
        st.json(directions_result)

    except Exception as e:
        st.error(f"Erreur lors de l'obtention des directions: {e}")

