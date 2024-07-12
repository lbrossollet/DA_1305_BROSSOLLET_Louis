import streamlit as st
import googlemaps
import json

# Définir votre clé API Google Maps
api_key = 'AIzaSyBND6dYdzOqlND5K-LQ2wJc0jBpUQIl2pQ'  # Remplacez 'YOUR_API_KEY' par votre clé API réelle

# Fonction pour initialiser Google Maps Client
def initialize_gmaps():
    try:
        return googlemaps.Client(key=api_key)
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation du client Google Maps : {e}")
        return None

# Fonction pour afficher l'itinéraire
def afficher_itineraire(origins_and_destinations, gmaps):
    try:
        # Préparer la requête Directions
        origin = origins_and_destinations[0]
        waypoints = origins_and_destinations[1:-1] if len(origins_and_destinations) > 2 else []
        destination = origins_and_destinations[-1]

        directions_result = gmaps.directions(origin, destination, mode="driving", waypoints=waypoints)
        steps = directions_result[0]['legs'][0]['steps']
        leg = directions_result[0]['legs'][0]

        # Extraire la distance et le temps total
        total_distance = leg['distance']['text']
        total_duration = leg['duration']['text']

        # Afficher la distance et le temps total
        st.subheader('Détails du trajet:')
        st.markdown(f"**Distance totale :** {total_distance}")
        st.markdown(f"**Durée totale :** {total_duration}")

        
        # Récupérer les coordonnées de l'itinéraire
        path_coords = []
        markers_coords = []
        for leg in directions_result[0]['legs']:
            markers_coords.append((leg['start_location']['lat'], leg['start_location']['lng']))
            for step in leg['steps']:
                polyline = step['polyline']['points']
                decoded_points = googlemaps.convert.decode_polyline(polyline)
                path_coords.extend(decoded_points)
            markers_coords.append((leg['end_location']['lat'], leg['end_location']['lng']))

        # Générer le code HTML pour intégrer Google Maps
        path_coords_js = [{"lat": point['lat'], "lng": point['lng']} for point in path_coords]
        markers_coords_js = [{"lat": point[0], "lng": point[1]} for point in markers_coords]
        path_coords_json = json.dumps(path_coords_js)
        markers_coords_json = json.dumps(markers_coords_js)

        html_code = f"""
        <html>
        <head>
            <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places"></script>
            <script>
                function initMap() {{
                    var map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 13,
                        center: {{lat: {markers_coords_js[0]['lat']}, lng: {markers_coords_js[0]['lng']}}}
                    }});

                    var pathCoords = {path_coords_json};
                    var markersCoords = {markers_coords_json};

                    var flightPath = new google.maps.Polyline({{
                        path: pathCoords,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                    }});

                    flightPath.setMap(map);

                    markersCoords.forEach(function(coord) {{
                        new google.maps.Marker({{
                            position: coord,
                            map: map
                        }});
                    }});
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
        # Afficher les détails entre les adresses
        st.subheader('Détails entre les adresses :')
        for i, step in enumerate(steps):
            instruction = step['html_instructions']
            distance = step['distance']['text']
            duration = step['duration']['text']
            if i > 0:
                st.markdown(f"<b>{instruction}</b> - {distance}, {duration}", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur lors de l'obtention des directions: {e}")

# Créer l'interface utilisateur avec Streamlit
st.title('API Google Maps Directions avec Streamlit')

# Initialisation de gmaps
gmaps = initialize_gmaps()

# Section pour la carte
st.header('Carte')
st.markdown('**Affichage de l\'itinéraire sur la carte :**')

# Entrée de l'utilisateur pour l'origine et la destination
st.header('Planifiez votre itinéraire')
origin = st.text_input('Origine', 'Châtelet, Paris')
destination = st.text_input('Destination', 'Tour Eiffel, Paris')

# Liste pour stocker les adresses supplémentaires
if 'additional_addresses' not in st.session_state:
    st.session_state.additional_addresses = []

# Ajouter la possibilité d'entrer d'autres adresses
st.header('Ajouter des adresses supplémentaires')
additional_address = st.text_input('Ajouter une autre adresse', 'Ex: 1600 Amphitheatre Parkway, Mountain View, CA')
if st.button('Ajouter l\'adresse'):
    st.session_state.additional_addresses.append(additional_address)
    st.success(f"Adresse ajoutée : {additional_address}")

# Afficher les adresses supplémentaires ajoutées
if st.session_state.additional_addresses:
    st.subheader('Adresses supplémentaires ajoutées :')
    for idx, address in enumerate(st.session_state.additional_addresses, 1):
        st.write(f"{idx}. {address}")

# Bouton pour obtenir les directions
if st.button('Obtenir les directions'):
    if gmaps is None:
        st.error("Erreur : Client Google Maps non initialisé.")
    else:
        all_addresses = [origin] + st.session_state.additional_addresses + [destination]
        afficher_itineraire(all_addresses, gmaps)

# Bouton pour entrer une nouvelle destination
if st.button('Entrer une nouvelle destination'):
    st.session_state.additional_addresses = []
    st.experimental_rerun()
