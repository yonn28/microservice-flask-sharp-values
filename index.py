from flask import Flask, jsonify, request
import pandas as pd
from urllib.request import urlopen
import joblib
import ssl
import json
import functions

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

#-----------------------------------------Models and DataBases-------------------------
##---------*Malnutrition*----------------
with urlopen('https://storage.googleapis.com/ds4all-test-bd1/Modelo_malnutrition.sav') as response:
    modelo_malnutrition = joblib.load(response)

base_malnutrition = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_malnutrition.csv').drop(["IdBeneficiario","Unnamed: 0","Unnamed: 0.1"],axis=1)

"""
-----------------------------------------Top 10 df-----------------------------------------------------
"""

#-----------------------------------------*Malnutrition*------------------------------
top10_df_m = functions.createTable_top(modelo_malnutrition, base_malnutrition)
p_range_m = str(top10_df_m["Range_probability"].iloc[0])
n_children_m = top10_df_m.shape[0]
shap_m = functions.plotShapValuesTop(modelo_malnutrition, top10_df_m)
s_table_m = functions.table_to_show(top10_df_m)
show_table_m = s_table_m[s_table_m['AVG ZScore'] > -100].sample(frac=0.05)


@app.route('/api/v2/mal_n', methods=['GET'])
def getting_dataframe_mal_n():
    return jsonify(n_children_m)

@app.route('/api/v2/mal_p', methods=['GET'])
def getting_dataframe_mal_p():
    return jsonify(p_range_m)

@app.route('/api/v2/shap_mal', methods=['GET'])
def getting_dataframe_shap_mal():
    return jsonify(shap_m)

@app.route('/api/v2/show_mal', methods=['GET'])
def getting_dataframe_mal():
    initial = int(request.headers.get('initial'))
    end = int(request.headers.get('end'))
    return jsonify(show_table_m[initial:end].to_dict("records"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) #change port to 8080 for deployment, and host = '0.0.0.0'
