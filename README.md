**SirenSight — Intelligent Emergency Vehicle Alert System**

**Overview**

SirenSight is an AI-powered real-time emergency alert system designed to detect approaching ambulances and notify nearby citizens and traffic authorities. It combines computer vision, audio recognition, and GPS-based intelligence to ensure faster and safer emergency response.

The system helps reduce delays for emergency vehicles by proactively alerting nearby users and enabling traffic management systems.

---

**Key Features**

*  Real-time ambulance detection using AI (YOLO)
*  Siren detection using audio classification (TensorFlow)
*  GPS-based proximity detection using Haversine distance
*  Multi-layer verification (Audio + Vision + GPS)
*  Instant alerts via Firebase Cloud Messaging
*  Traffic junction alert system for authorities
*  Android app integration for citizen notifications

---

**System Architecture**

<img width="893" height="454" alt="image" src="https://github.com/user-attachments/assets/3467a502-a5df-4c48-8f23-08ee38252f76" />


---

**Tech Stack**

**AI & Backend**

* Python
* OpenCV
* YOLO (Ultralytics)
* TensorFlow (Audio Model)

**Cloud & Realtime**

* Firebase Realtime Database
* Firebase Cloud Messaging

**Mobile**

* Android (Java)

**Other**

* Haversine Algorithm (Distance Calculation)
* Multithreading for real-time processing

---

**How It Works**

1. Camera detects vehicles using YOLO
2. Audio model detects ambulance siren
3. GPS data of ambulance is fetched from Firebase
4. Distance and direction are calculated using Haversine + Bearing
5. System validates using:

   * Audio (mandatory)
   * Vision OR GPS proximity
6. If conditions are met:

   * Alerts are triggered for nearby users
   * Traffic junction status is updated

---

**Setup Instructions**

**Backend (Python)**

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Add Firebase credentials:

   * Place `serviceAccount.json` in project root
4. Add model files:

   * `best.pt` (YOLO model)
   * `siren_ear.h5` (audio model)
5. Run:

   ```bash
   python main.py
   ```

---

**Android App**

1. Open project in Android Studio
2. Add Firebase config:

   * Place `google-services.json` inside `/app`
3. Run on device/emulator

---


**Screenshots**

<img width="255" height="581" alt="image" src="https://github.com/user-attachments/assets/162cb2fa-72f2-4206-8b37-5d2b136b8498" /> <img width="254" height="578" alt="image" src="https://github.com/user-attachments/assets/9472970b-dda7-49cc-9b65-fc8d5a8963ea" />
<img width="251" height="573" alt="image" src="https://github.com/user-attachments/assets/6117c4f1-9358-47f9-9249-fdd5c5b7f2fb" /> <img width="250" height="570" alt="image" src="https://github.com/user-attachments/assets/ef3027a3-3154-432e-b6f9-9f314a07b47f" />
<img width="286" height="652" alt="image" src="https://github.com/user-attachments/assets/0f593f3b-aa42-4575-a043-a204d6960d2a" /> <img width="369" height="659" alt="image" src="https://github.com/user-attachments/assets/72e9b172-940f-46f4-8ba7-0168c259a993" />
<img width="975" height="516" alt="image" src="https://github.com/user-attachments/assets/8204898a-1742-4074-a7e5-70063caea703" />
<img width="975" height="953" alt="image" src="https://github.com/user-attachments/assets/e988ef39-e8a8-47e5-b7b3-360f4261e645" />





---

**Future Improvements**

* Real-time traffic light control integration
* Edge device deployment (Raspberry Pi / Jetson)
* Advanced siren classification using deep learning
* Integration with smart city infrastructure

---

## 👨‍💻 Author

Maneeth Vigneswaran
