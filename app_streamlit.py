import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données depuis le fichier CSV
file_path = 'data_processed/df_filtered_north_zone.csv'
df = pd.read_csv(file_path, parse_dates=['Date_et_heure_de_comptage'])

# Calcul de la semaine de l'année
df['semaine'] = pd.to_datetime(df['Date_et_heure_de_comptage']).dt.isocalendar().week

# Titre de l'application
st.title('Statistiques de trafic à Paris')

# Répartition du débit horaire par semaine et par arrondissement
st.header('Répartition du débit horaire par semaine et par arrondissement')
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(data=df, x='semaine', y='Débit_horaire', estimator='mean', ci=None, hue='C_AR', ax=ax)
ax.set_xlabel('Semaine de l\'année')
ax.set_ylabel('Débit horaire moyen')
st.pyplot(fig)

# Affichage des données brutes pour référence
st.header('Données brutes (échantillon)')
st.write(df.head())

# Affichage des statistiques descriptives
st.header('Statistiques descriptives')
st.write(df.describe())

# Affichage des informations sur les colonnes
st.header('Informations sur les colonnes')
st.write(df.info())
