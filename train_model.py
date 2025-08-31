# File: train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model():
    """
    Loads fire data, trains a Random Forest Classifier model, and saves it to a file.
    """
    print("--- Starting Model Training ---")

    # 1. Load the Dataset
    try:
        df = pd.read_csv('sensor_dataset_balanced.csv')
        print("✅ Dataset 'sensor_dataset_balanced.csv' loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: 'sensor_dataset_balanced.csv' not found. Please place it in the same directory.")
        return

    # 2. Separate features (X) and target (y)
    X = df[['temperature', 'air_quality', 'smoke', 'flame']]
    y = df['fire']

    # 3. Create and Train the Random Forest Classifier Model
    # A Random Forest is an ensemble model that builds multiple decision trees
    # and merges them for better predictive accuracy.
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    print("⏳ Training the Random Forest model on the entire dataset...")
    model.fit(X, y)
    print("✅ Model training complete.")

    # 4. Save the Trained Model to a File
    filename = 'fire_detection_model.joblib'
    joblib.dump(model, filename)
    print(f"✅ Trained model saved to '{filename}'.")

if __name__ == "__main__":
    train_and_save_model()
