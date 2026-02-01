import sys
import os
import joblib
import pandas as pd
import numpy as np

# Adjust path to find modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security_simulation.attack_scenarios import generate_packet, manager
from security_simulation.feature_extractor import extract
from backend.ml_quantum.preprocess import preprocess

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_quantum/rf_ids_model.pkl")

def debug():
    print("🔍 Loading Model...")
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        return

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    selected_features = bundle["selected_features"]
    encoders = bundle["encoders"]
    scaler = bundle["scaler"]
    
    print(f"✅ Model Loaded. Expecting {len(selected_features)} features: {selected_features}")

    # Force "Normal" scenario
    print("\n🧪 Generating 'Normal' Traffic Sample...")
    
    # Hack to force normal scenario in generation
    # We will just manually create a 'Normal' style packet if the manager doesn't cooperate, 
    # but let's try to simulate the extracted features directly for a "Normal" web request.
    
    # 1. Simulate a Normal HTTP Request
    # Packet Stream Simulation
    print("   Generating stream of packets...")
    
    # We need to simulate a few packets to get the 'rate' feature from extractor
    packets = []
    from types import SimpleNamespace
    import time
    
    src_ip = "192.168.1.50"
    
    # Simulate 10 packets over 1 second (Normal rate)
    for i in range(10):
        p = SimpleNamespace(
            ip=SimpleNamespace(src=src_ip),
            tcp=SimpleNamespace(dstport=443),
            length=1000 if i % 2 == 0 else 60,
            ttl=64,
            proto="tcp"
        )
        packet_features = extract(p) # This aggregates
        # We need to sleep to simulate time passing for rate calc
        time.sleep(0.1) 
        
    # Valid features are in the last extraction (buffer full)
    if not packet_features:
        print("❌ feature_extractor returned None (buffer not full?)")
        return

    print("\n📊 Extracted Features (Key Counts):")
    keys_to_check = ["ct_srv_src", "ct_dst_ltm", "ct_src_dport_ltm", "sttl", "dbytes", "rate"]
    for k in keys_to_check:
        print(f"   {k}: {packet_features.get(k)}")

    # 2. DataFrame Construction
    df = pd.DataFrame([packet_features])
    
    # 3. Preprocess
    print("\n⚙️ Preprocessing...")
    
    # Ensure all model features exist or are 0
    for f in selected_features:
        if f not in df.columns:
            print(f"⚠️ Missing Feature: {f} (Setting to 0)")
            df[f] = 0
            
    # Apply Preprocessing (Encode/Scale)
    # We need to call preprocess logic manually or rely on the function if it handles 'fit=False' correctly
    # detailed inspect of preprocess.py suggests it handles inference
    
    # CRITICAL: Preprocess needs ALL features the scaler was trained on
    all_trained_features = bundle["features"]
    
    X_processed = preprocess(df, fit=False, encoders=encoders, scaler=scaler, features=all_trained_features)
    
    # 3b. FILTER to selected features for the model
    print(f"\nSubset to {len(selected_features)} selected features...")
    X_processed = X_processed[selected_features]
    
    # 4. Predict
    print("\n🔮 Prediction:")
    probs = model.predict_proba(X_processed)[0]
    classes = model.classes_
    
    # Show top 3
    top_indices = np.argsort(probs)[::-1][:3]
    for idx in top_indices:
        print(f"   {classes[idx]}: {probs[idx]:.4f}")
        
    pred = model.predict(X_processed)[0]
    print(f"\n✅ Final Classification: {pred}")

if __name__ == "__main__":
    debug()
