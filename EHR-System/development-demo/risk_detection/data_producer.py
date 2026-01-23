from sdv.metadata import Metadata
import pandas as pd
from sdv.single_table import CTGANSynthesizer
import os
import requests

CONSCIOUSNESS_MAPPING = {
    'A': 0,
    'C': 1,
    'V': 2, 
    'P': 3, 
    'U': 4
}

URL = "http://localhost:5000/calculate_risk"

data_path = os.path.join(os.path.dirname(__file__), "Health_Risk_Dataset.csv")
df = pd.read_csv(data_path, sep=",")

# Preprocess data similarily to training script
df = df.drop(columns=["Patient_ID", "Risk_Level"], errors="ignore")
df = df.drop_duplicates(keep='first') # Remove duplicates
df['Consciousness'] = df['Consciousness'].map(CONSCIOUSNESS_MAPPING)

# https://github.com/SaiSatya16/Synthetic-Data-Generation-using-CTGAN
metadata = Metadata.load_from_json(os.path.join(os.path.dirname(__file__), "metadata.json"))
synthesizer = CTGANSynthesizer(
    metadata=metadata,
    epochs=70
)
synthesizer.fit(df)

def post_entry(entry: dict):
    response = requests.post(URL, json=entry)
    return response.json()

def create_and_send_entries(num_of_entries: int):
    synthetic_data = synthesizer.sample(num_rows=num_of_entries)
    for _, row in synthetic_data.iterrows():
        response = post_entry(row.to_dict())
        print(f"Response: {response}")

if __name__ == "__main__":
    create_and_send_entries(50)