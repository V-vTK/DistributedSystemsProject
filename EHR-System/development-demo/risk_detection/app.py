import os
from flask import jsonify, Flask
import flask
import joblib
import pandas as pd

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), 'model', 'risk_model.pkl')
model = joblib.load(model_path)

# https://www.kaggle.com/code/ludocielbeckett/health-risk-prediction-98
def predict_risk_score(data: dict):
    data = pd.DataFrame([{
        'Respiratory_Rate': data['Respiratory_Rate'],
        'Oxygen_Saturation': data['Oxygen_Saturation'],
        'O2_Scale': data['O2_Scale'],
        'Systolic_BP': data['Systolic_BP'],
        'Heart_Rate': data['Heart_Rate'],
        'Temperature': data['Temperature'],
        'Consciousness': data['Consciousness'],
        'On_Oxygen': data['On_Oxygen']
    }])
    pred_rf = model.predict(data)[0]
    return pred_rf

@app.route("/health")
def health():
    return {"Health": "OK"}, 200

@app.route("/calculate_risk", methods=['POST'])
def calculate_risk():
    json_data = flask.request.get_json()
    try:
        risk_score = predict_risk_score(json_data)
    except (KeyError, ValueError) as e:
        return jsonify("Invalid input data", str(e)), 400
    except Exception as e:
        return jsonify("General error processing request", str(e)), 500
    return {"risk_score": int(risk_score)}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
