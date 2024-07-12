from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import holidays

app = Flask(__name__)

# Chargement du modèle
model = joblib.load('modele_traffic.pkl')

# Prétraitement des données
cat_features = ['C_AR', 'AM/PM']
numeric_features = ['Identifiant_arc', 'annee', 'mois', 'jour', 'vacances', 'semaine']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), cat_features),
        ('num', 'passthrough', numeric_features)
    ]
)

def get_weekday_and_week(date_str):
    from datetime import datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')
    weekday = date.strftime('%A')
    week_number = date.strftime('%W')
    return weekday, int(week_number)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    
    date_str = data['date']
    weekday, week_number = get_weekday_and_week(date_str)
    
    prediction_data = {
        'Identifiant_arc': data['Identifiant_arc'],
        'C_AR': data['C_AR'],
        'AM/PM': data['AM/PM'],
        'annee': int(date_str[:4]),
        'mois': int(date_str[5:7]),
        'jour': int(date_str[8:10]),
        'vacances': 1 if date_str in holidays.France() else 0,
        'semaine': week_number
    }
    
    prediction_df = pd.DataFrame([prediction_data])
    prediction_df_preprocessed = preprocessor.transform(prediction_df)
    prediction = model.predict(prediction_df_preprocessed)
    
    result = {
        'Identifiant_arc': data['Identifiant_arc'],
        'C_AR': data['C_AR'],
        'AM/PM': data['AM/PM'],
        'Etat_trafic_mean': prediction[0]
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
