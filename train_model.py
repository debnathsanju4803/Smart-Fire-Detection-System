# File: train_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
import joblib

def train_and_save_model():
    """
    Loads fire data, trains a voting ensemble model, and saves it to a file.
    """
    print("--- Starting Model Training ---")
    
    # 1. Load the Dataset
    try:
        df = pd.read_csv('fire_data.csv')
        print("✅ Dataset 'fire_data.csv' loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: 'fire_data.csv' not found. Please place it in the same directory.")
        return

    X = df[['temperature', 'smoke']]
    y = df['fire']

    # 2. Initialize the Base Models
    model_lr = LogisticRegression(random_state=42)
    model_svm = SVC(random_state=42)
    model_dt = DecisionTreeClassifier(random_state=42)
    print("✅ Base models (LR, SVM, DT) initialized.")

    # 3. Create and Train the Voting Ensemble Model
    # We train on the *entire* dataset to make the final model as knowledgeable as possible.
    ensemble_model = VotingClassifier(
        estimators=[('lr', model_lr), ('svm', model_svm), ('dt', model_dt)],
        voting='hard'
    )
    print("⏳ Training the final ensemble model on the entire dataset...")
    ensemble_model.fit(X, y)
    print("✅ Model training complete.")

    # 4. Save the Trained Model to a File
    filename = 'fire_detection_model.joblib'
    joblib.dump(ensemble_model, filename)
    print(f"🚀 Model has been saved to '{filename}'.")
    print("--- Model Training Finished ---")

if __name__ == '__main__':
    train_and_save_model()
