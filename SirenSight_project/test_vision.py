from ultralytics import YOLO

# Load your model
model = YOLO('best.pt')

# Open your webcam and start detecting
# source=0 is your laptop's camera
model.predict(source=0, show=True, conf=0.6)