import streamlit as st
import googlemaps
import pydeck as pdk

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

        # Coordonnées de départ et d'arrivée pour Pydeck
        start_coords = (directions_result[0]['legs'][0]['start_location']['lat'], directions_result[0]['legs'][0]['start_location']['lng'])
        end_coords = (directions_result[0]['legs'][0]['end_location']['lat'], directions_result[0]['legs'][0]['end_location']['lng'])

        # Créer une vue Pydeck avec une carte
        view_state = pdk.ViewState(
            latitude=start_coords[0],
            longitude=start_coords[1],
            zoom=12,
            pitch=50
        )

        # Créer une ligne pour représenter l'itinéraire
        line_layer = pdk.Layer(
            'PathLayer',
            data=[{
                'path': [start_coords, end_coords],
                'widthScale': 5,
                'widthMinPixels': 5,
                'widthMaxPixels': 10,
                'getColor': [255, 0, 0],
            }],
        )

        # Créer la carte Pydeck
        fig = pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=view_state,
            layers=[line_layer],
        )

        # Afficher la carte dans Streamlit
        st.pydeck_chart(fig)

    except Exception as e:
        st.error(f"Erreur lors de l'obtention des directions: {e}")
