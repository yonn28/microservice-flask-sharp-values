from flask import Flask, jsonify
import pandas as pd
from itertools import cycle
from flask_cors import CORS
from flask_sslify import SSLify
from urllib.request import urlopen
import joblib
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

#-----------------------------------------Models and DataBases-------------------------
##---------*Malnutrition*----------------
with urlopen('https://storage.googleapis.com/ds4all-test-bd1/Modelo_malnutrition.sav') as response:
    modelo_malnutrition = joblib.load(response)

base_malnutrition = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_malnutrition.csv').drop(["IdBeneficiario","Unnamed: 0","Unnamed: 0.1"],axis=1)
##-----------*Relapse*----------------
with urlopen('https://storage.googleapis.com/ds4all-test-bd1/Modelo_relapse.sav') as response:
    modelo_relapse = joblib.load(response)

base_relapse = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_relapse.csv').drop(["IdBeneficiario","Unnamed: 0"],axis=1)

#-----------------------------------------Top 10 df-------------------------

def createTable_top(objeto_modelo, base_variables):
    # Create a new column with the predicted probability:

    base_variables.loc[:, "Probability"] = objeto_modelo.predict_proba(base_variables)[:, 1]
    base_variables = base_variables.sort_values("Probability", ascending=False)

    # Create a column with the range of the probability:

    base_variables.loc[:, "Range_probability"] = pd.qcut(base_variables['Probability'], q=10, precision=0,
                                                         duplicates='drop')
    # Top 10%

    a = pd.DataFrame(base_variables.groupby(["Range_probability"]).size().reset_index()).rename(columns={0: 'Total'})
    buscado = a.loc[9, "Range_probability"]

    c_df = base_variables[base_variables["Range_probability"] == buscado]
    cols = ['MIN_ZScorePesoTalla_12M', 'AVG_ZScorePesoTalla_12M', 'MAX_ZScorePesoTalla_12M', 'Veces_DesnutricionSM_12M',
            'Veces_SobrePeso_12M', 'Veces_Normal_12M', 'TienePasado', 'sexo_persona_1.0',
            'tip_cuidado_niños_2.0', 'tip_cuidado_niños_3.0', 'tip_cuidado_niños_4.0', 'tip_cuidado_niños_5.0',
            'tip_cuidado_niños_6.0', 'tip_cuidado_niños_7.0', 'tip_cuidado_niños_8.0', 'tip_cuidado_niños_9.0',
            'ingresos_promp_imp', 'uni_dias_agua', 'cod_clase_2.0', 'cod_clase_3.0', 'noprivaciones', 'ind_estudia_1.0',
            'estrato_1.0', 'estrato_2.0', 'estrato_3.0', 'estrato_4.0', 'estrato_5.0', 'estrato_6.0', 'Probability',
            'Range_probability']
    df = c_df.copy()
    df = df[cols]

    return (df)

top10_mal = createTable_top(modelo_malnutrition, base_malnutrition)
top10_rel = createTable_top(modelo_relapse, base_relapse)

@app.route('/api/v2/mal', methods=['GET'])
def getting_dataframe_mal():
    top10_mal["Range_probability"] = top10_mal["Range_probability"].astype(str)
    # print(top10_mal)
    return json.dumps(top10_mal.to_dict("records"))

@app.route('/api/v2/rel', methods=['GET'])
def getting_dataframe_rel():
    top10_rel["Range_probability"] = top10_rel["Range_probability"].astype(str)
    # print(top10_mal)
    return json.dumps(top10_rel.to_dict("records"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) #change port to 8080 for deployment, and host = '0.0.0.0'
    # app.run(debug=True, port=3000) #change port to 8080 for deployment, and host = '0.0.0.0'