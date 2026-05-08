from tensorflow.keras.models import load_model

# Load old model
model = load_model("app/ml/papaya_model.h5", compile=False)

# Save again in compatible format
model.save("app/ml/papaya_model_fixed.h5")