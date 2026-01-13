
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any

MODEL_PATH = os.getenv("MODEL_PATH", "model_rf.joblib")
SCALER_PATH = os.getenv("SCALER_PATH", "scaler.joblib")

class MLEngine:
	def __init__(self):
		self.model = None
		self.scaler = None
		self.feature_names = None
		self.load_model()

	def load_model(self):
		if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
			self.model = joblib.load(MODEL_PATH)
			self.scaler = joblib.load(SCALER_PATH)
			self.feature_names = getattr(self.model, 'feature_names_in_', None)
		else:
			# For MVP: create a dummy model (not trained)
			self.model = RandomForestClassifier(n_estimators=10)
			self.scaler = StandardScaler()
			self.feature_names = []

	def predict(self, features: Dict[str, Any]):
		if not self.model or not self.scaler or not self.feature_names:
			return {"error": "Model not loaded or trained."}
		X = np.array([[features.get(f, 0) for f in self.feature_names]])
		X_scaled = self.scaler.transform(X)
		pred = self.model.predict(X_scaled)[0]
		proba = self.model.predict_proba(X_scaled)[0].max()
		explanation = self.explain(X_scaled)
		return {"prediction": int(pred), "confidence": float(proba), "explanation": explanation}

	def explain(self, X):
		# Feature importance for Random Forest or Logistic Regression
		if hasattr(self.model, "feature_importances_"):
			importances = self.model.feature_importances_
		elif hasattr(self.model, "coef_"):
			importances = np.abs(self.model.coef_[0])
		else:
			importances = np.zeros(len(self.feature_names))
		return dict(zip(self.feature_names, importances))

ml_engine = MLEngine()
