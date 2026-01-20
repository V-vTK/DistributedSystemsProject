import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import joblib

# Dataset from Kaggle: https://www.kaggle.com/datasets/ludocielbeckett/health-risk-prediction-anonymized-real-data/data?select=Health_Risk_Dataset.csv
# Based on https://www.kaggle.com/code/ludocielbeckett/health-risk-prediction-98
class TrainRiskModel:

    def __init__(self, data_path, output_path="model"):
        self.df = pd.read_csv(data_path, sep=",")
        self.output_path = output_path
        self.model = None
        if "Risk_Level" not in self.df.columns:
            raise Exception("Dataset must contain target column 'Risk_Level'")

    def preprocess_data(self):
        self.df = self.df.drop_duplicates(keep='first') # Remove duplicates
        self.df = self.df.drop(columns=["Patient_ID"]) # Drop identifier column not needed for training
        self.df['Risk_Level'] = self.df['Risk_Level'].map(self._get_risk_mapping()) # Make numerical
        _get_consciousness_mapping = self._get_consciousness_mapping() # Make numerical
        self.df['Consciousness'] = self.df['Consciousness'].map(_get_consciousness_mapping)

    def create_train_test_split(self, test_size=0.2):
        self.features = self.df.drop(columns=["Risk_Level"])
        self.target_column = self.df["Risk_Level"]
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.target_column, test_size=test_size, random_state=50, stratify=self.target_column)
        return X_train, X_test, y_train, y_test

    def train_model(self, logging=False):
        # Random Forest Classifier
        X_train, X_test, y_train, y_test = self.create_train_test_split()
        rf = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 50)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        if logging:
            print("Accuracy:", accuracy_score(y_test, y_pred_rf))
            print("F1_score:", f1_score(y_test, y_pred_rf, average='weighted'))
            print(classification_report(y_test, y_pred_rf))
        self.model = rf
        return rf

    def output_model(self, name: str):
        # https://stackoverflow.com/questions/56107259/how-to-save-a-trained-model-by-scikit-learn
        if self.model is None:
            raise Exception("Model not trained yet. Call train_model() before saving the model.")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        model_path = os.path.join(self.output_path, name)
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, path: str):
        # https://stackoverflow.com/questions/56107259/how-to-save-a-trained-model-by-scikit-learn
        self.model = joblib.load(path)
        print(f"Model loaded from {path}")

    def describe_dataset(self):
        print(self.df.head())
        print(self.df.describe())
        print(self.df.info())
        
    def _get_categories(self):
        return list(self.df["Risk_Level"].unique())

    def _get_risk_mapping(self):
        risk_mapping = {
            'Normal': 0,
            'Low': 1,
            'Medium': 2,
            'High': 3
        }
        return risk_mapping
    
    def _get_consciousness_mapping(self):
        # https://ckm.openehr.org/ckm/archetypes/1013.1.3317
        # ACVPU is an acronym for 'Alert', 'Confusion', 'Voice', 'Pain', 'Unresponsive'.
        conscious_mapping = {
            'A': 0,
            'C': 1,
            'V': 2, 
            'P': 3, 
            'U': 4
        }
        return conscious_mapping

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "Health_Risk_Dataset.csv")
    output_path = os.path.join(os.path.dirname(__file__), "model")
    trainer = TrainRiskModel(data_path, output_path)
    trainer.preprocess_data()
    # trainer.describe_dataset()
    trainer.train_model()
    trainer.output_model("risk_model.pkl")
    print(trainer._get_categories())


# Syntetic data generation
# https://www.datacamp.com/tutorial/synthetic-data-generation
# https://docs.sdv.dev/sdv/single-table-data/modeling/synthesizers/ctgansynthesizer