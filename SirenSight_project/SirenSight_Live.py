import cv2
from ultralytics import YOLO

# 1. Load your trained 'brain' (Make sure best.pt is in the same folder as this script)
model = YOLO('best.pt')

# 2. Open the Laptop Webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

print("🚀 SirenSight Live Detection Started...")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 3. Run the AI model on the current frame
    # We set a confidence of 0.6 to avoid flickering false alarms
    results = model.predict(frame, conf=0.6, show=False)

    # 4. Check if an ambulance is detected
    ambulance_detected = False
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            if class_id == 0:  # 0 is our 'Ambulance' class
                ambulance_detected = True
                # Draw a special red alert on the screen
                cv2.putText(frame, "🚨 AMBULANCE DETECTED! 🚨", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # 5. Show the live feed
    annotated_frame = results[0].plot()
    cv2.imshow("SirenSight - Junction Laptop Feed", annotated_frame)

    # Press 'q' to stop the feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()