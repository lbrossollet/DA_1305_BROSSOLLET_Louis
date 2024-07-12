import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
df = pd.read_csv('data_processed/traffic_shift_nord.csv')

# Sidebar pour sélectionner l'arrondissement
arrondissements = df['C_AR'].unique()
selected_arrondissement = st.sidebar.selectbox('Sélectionner un arrondissement', arrondissements)

# Filtrer les données par arrondissement sélectionné
df_selected = df[df['C_AR'] == selected_arrondissement]

# Titre de l'application Streamlit
st.title('Visualisation du Trafic')

# 1. État du trafic par semaine
st.subheader('État du Trafic par Semaine')

# Calculer la moyenne du Débit Horaire par semaine
average_weekly_traffic = df.groupby('semaine')['Débit_horaire'].mean().reset_index()

# Graphique avec seaborn
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(x='semaine', y='Débit_horaire', data=average_weekly_traffic, ax=ax1)
ax1.set_title('Moyenne du Débit Horaire par Semaine')
ax1.set_xlabel('Semaine')
ax1.set_ylabel('Moyenne du Débit Horaire')
st.pyplot(fig1)

# 2. État du trafic par jour de la semaine
st.subheader('État du Trafic par Jour de la Semaine')

# Calculer la moyenne du Débit Horaire par jour de la semaine
average_daily_traffic = df.groupby('jour')['Débit_horaire'].mean().reset_index()

# Graphique avec seaborn
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='jour', y='Débit_horaire', data=average_daily_traffic, ax=ax2)
ax2.set_title('Moyenne du Débit Horaire par Jour de la Semaine')
ax2.set_xlabel('Jour de la Semaine')
ax2.set_ylabel('Moyenne du Débit Horaire')
st.pyplot(fig2)

# 3. Débit horaire moyen par arrondissement
st.subheader('Débit Horaire Moyen par Arrondissement')

# Calculer la moyenne du Débit Horaire par arrondissement
average_traffic_by_arrondissement = df.groupby('C_AR')['Débit_horaire'].mean().reset_index()

# Graphique avec seaborn
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='C_AR', y='Débit_horaire', data=average_traffic_by_arrondissement, ax=ax3)
ax3.set_title('Débit Horaire Moyen par Arrondissement')
ax3.set_xlabel('Arrondissement')
ax3.set_ylabel('Moyenne du Débit Horaire')
st.pyplot(fig3)

# 4. Taux d'occupation moyen par arrondissement
st.subheader('Taux d\'Occupation Moyen par Arrondissement')

# Calculer la moyenne du Taux d'Occupation par arrondissement
average_occupation_by_arrondissement = df.groupby('C_AR')["Taux_d'occupation"].mean().reset_index()

# Graphique avec seaborn
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='C_AR', y="Taux_d'occupation", data=average_occupation_by_arrondissement, ax=ax4)
ax4.set_title('Taux d\'Occupation Moyen par Arrondissement')
ax4.set_xlabel('Arrondissement')
ax4.set_ylabel('Moyenne du Taux d\'Occupation')
st.pyplot(fig4)

# 5. Débit horaire moyen par AM/PM et jour de la semaine pour l'arrondissement sélectionné
st.subheader(f'Débit Horaire Moyen par AM/PM et par Jour de la Semaine - Arrondissement {selected_arrondissement}')

# Calculer la moyenne du Débit Horaire par AM/PM et par jour de la semaine pour l'arrondissement sélectionné
average_traffic_arr = df_selected.groupby(['AM/PM', 'jour'])['Débit_horaire'].mean().reset_index()

# Graphique avec seaborn
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(x='jour', y='Débit_horaire', hue='AM/PM', data=average_traffic_arr, ax=ax5)
ax5.set_title(f'Moyenne du Débit Horaire par AM/PM et par Jour de la Semaine - Arrondissement {selected_arrondissement}')
ax5.set_xlabel('Jour de la Semaine')
ax5.set_ylabel('Moyenne du Débit Horaire')
st.pyplot(fig5)
