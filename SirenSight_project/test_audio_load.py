import tensorflow as tf

# Try to load the model
try:
    model = tf.keras.models.load_model('siren_ear.h5')
    print("✅ AUDIO BRAIN LOADED SUCCESSFULLY!")
except Exception as e:
    print(f"❌ ERROR: {e}")