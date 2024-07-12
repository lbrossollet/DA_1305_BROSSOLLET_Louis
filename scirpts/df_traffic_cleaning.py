import pandas as pd

def main():
    # Charger les données depuis le fichier CSV
    df_traffic = pd.read_csv('../data/traffic_data.csv', sep=';')

    # Remplacer les espaces dans les titres de colonnes par des underscores
    df_traffic.columns = df_traffic.columns.str.replace(' ', '_')

    # Création du premier DataFrame avec les colonnes sélectionnées, suppression des NaN et des doublons
    columns_selected = [
        'Identifiant_arc', 'Libelle', 'Date_et_heure_de_comptage', 
        'Débit_horaire', 'Taux_d\'occupation', 'Etat_trafic'
    ]
    df_selected = df_traffic[columns_selected].dropna().drop_duplicates()

    # Sauvegarder le premier DataFrame en fichier CSV
    df_selected.to_csv('../data/traffic_data_selected.csv', index=False)

    # Création du second DataFrame avec les colonnes sélectionnées, suppression des NaN et des doublons
    df_geo = df_traffic[['Identifiant_arc', 'geo_point_2d']].dropna().drop_duplicates()

    # Séparation des coordonnées géographiques en latitude et longitude
    df_geo[['Latitude', 'Longitude']] = df_geo['geo_point_2d'].str.split(', ', expand=True)

    # Conversion des colonnes Latitude et Longitude en type float
    df_geo['Latitude'] = df_geo['Latitude'].astype(float)
    df_geo['Longitude'] = df_geo['Longitude'].astype(float)

    # Sélectionner uniquement les colonnes nécessaires pour le second DataFrame
    df_geo = df_geo[['Identifiant_arc', 'Latitude', 'Longitude']]

    # Sauvegarder le second DataFrame en fichier CSV
    df_geo.to_csv('../data/traffic_data_geo.csv', index=False)

    print("Les fichiers CSV ont été créés avec succès.")

if __name__ == "__main__":
    main()
