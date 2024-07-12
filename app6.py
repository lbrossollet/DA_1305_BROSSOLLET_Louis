import streamlit as st
import googlemaps
import json

# Définir votre clé API Google Maps
api_key = 'AIzaSyBND6dYdzOqlND5K-LQ2wJc0jBpUQIl2pQ' # Remplacez 'YOUR_API_KEY' par votre clé API réelle
gmaps = googlemaps.Client(key=api_key)

# Fonction pour obtenir et afficher l'itinéraire sur la carte
def afficher_itineraire(origin, destination):
    try:
        # Faire une requête à l'API Directions
        directions_result = gmaps.directions(origin, destination, mode="driving")
        steps = directions_result[0]['legs'][0]['steps']

        # Afficher les étapes de l'itinéraire
        st.subheader('Étapes de l\'itinéraire:')
        for step in steps:
            st.markdown(f"{step['html_instructions']} - {step['distance']['text']}, {step['duration']['text']}")

        # Récupérer les coordonnées de l'itinéraire
        path_coords = []
        for step in steps:
            polyline = step['polyline']['points']
            decoded_points = googlemaps.convert.decode_polyline(polyline)
            path_coords.extend(decoded_points)

        # Générer le code HTML pour intégrer Google Maps
        path_coords_js = [{"lat": point['lat'], "lng": point['lng']} for point in path_coords]
        path_coords_json = json.dumps(path_coords_js)

        html_code = f"""
        <html>
        <head>
            <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places"></script>
            <script>
                function initMap() {{
                    var map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 13,
                        center: {{lat: {path_coords_js[0]['lat']}, lng: {path_coords_js[0]['lng']}}}
                    }});

                    var directionsService = new google.maps.DirectionsService;
                    var directionsRenderer = new google.maps.DirectionsRenderer({{
                        map: map,
                        suppressMarkers: true
                    }});

                    var pathCoords = {path_coords_json};

                    var flightPath = new google.maps.Polyline({{
                        path: pathCoords,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    }});

                    flightPath.setMap(map);
                }}
            </script>
        </head>
        <body onload="initMap()">
            <div id="map" style="height: 600px; width: 100%;"></div>
        </body>
        </html>
        """

        # Intégrer le code HTML dans Streamlit
        st.components.v1.html(html_code, height=600)

    except Exception as e:
        st.error(f"Erreur lors de l'obtention des directions: {e}")

# Créer l'interface utilisateur avec Streamlit
st.title('API Google Maps Directions avec Streamlit')

# Section pour la carte
st.header('Carte')
st.markdown('**Affichage de l\'itinéraire sur la carte :**')

# Entrée de l'utilisateur pour l'origine et la destination
st.header('Planifiez votre itinéraire')
origin = st.text_input('Origine', 'Châtelet, Paris')
destination = st.text_input('Destination', 'Tour Eiffel, Paris')

# Bouton pour obtenir les directions
if st.button('Obtenir les directions'):
    afficher_itineraire(origin, destination)

# Bouton pour entrer une nouvelle destination
if st.button('Entrer une nouvelle destination'):
    origin = st.text_input('Nouvelle origine', 'Châtelet, Paris', key='new_origin')
    destination = st.text_input('Nouvelle destination', 'Tour Eiffel, Paris', key='new_destination')
    if st.button('Obtenir les nouvelles directions'):
        afficher_itineraire(origin, destination)

# Ajouter la possibilité d'entrer d'autres adresses
st.header('Ajouter des adresses supplémentaires')
additional_address = st.text_input('Ajouter une autre adresse', 'Ex: 1600 Amphitheatre Parkway, Mountain View, CA')
if st.button('Ajouter l\'adresse'):
    st.write(f"Adresse ajoutée : {additional_address}")
