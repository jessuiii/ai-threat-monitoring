import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from ml_quantum.preprocess import preprocess

# Load trained model bundle
bundle = joblib.load("ml/rf_ids_model.pkl")

rf_model = bundle["model"]
FEATURES = bundle["features"]
encoders = bundle["encoders"]
scaler = bundle["scaler"]

# Load TEST dataset
df_test = pd.read_csv("dataset/raw/test.csv")

# Preprocess test data (NO FITTING)
X_test, y_test = preprocess(
    df_test,
    fit=False,
    encoders=encoders,
    scaler=scaler
)

# Ensure same feature order
X_test = X_test[FEATURES]

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluation metrics
print("\n📊 MODEL EVALUATION RESULTS\n")

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
