import joblib
import os
import sys

# Adjust path to find modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

MODEL_PATH = os.path.join("backend", "ml_quantum", "rf_ids_model.pkl")

def check_features():
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        return

    print(f"📂 Loading model from {MODEL_PATH}...")
    bundle = joblib.load(MODEL_PATH)
    
    selected = bundle.get("selected_features", [])
    print(f"\n✅ Model was trained on {len(selected)} features:")
    for i, f in enumerate(selected, 1):
        print(f"   {i}. {f}")

    # Check if these exist in the extractor code (manual check or we can import)
    from security_simulation.feature_extractor import extract
    from types import SimpleNamespace
    import time
    
    print("\n🧪 Testing Feature Extractor coverage...")
    # Mock packet
    p = SimpleNamespace(
        ip=SimpleNamespace(src="1.1.1.1"),
        tcp=SimpleNamespace(dstport=80),
        length=100,
        ttl=64,
        proto="tcp"
    )
    
    # We need to call it a few times to fill buffer
    features = None
    for _ in range(6):
        features = extract(p)
        time.sleep(0.001)
        
    if features:
        print("   Extractor keys:", list(features.keys()))
        missing = [f for f in selected if f not in features]
        if missing:
            print(f"❌ MISSING Features in functionalities: {missing}")
        else:
            print("✅ ALL 20 features are present in the simulation!")
    else:
        print("❌ Could not extract features from simulation.")

if __name__ == "__main__":
    check_features()
