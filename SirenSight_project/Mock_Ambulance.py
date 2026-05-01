import firebase_admin
from firebase_admin import credentials, db
import time

# ==========================================
# 1. FIREBASE SETUP
# ==========================================
SERVICE_ACCOUNT_KEY = "serviceAccount.json"
DATABASE_URL = "https://sirensight-9a4e8-default-rtdb.firebaseio.com/"

print("Starting Dynamic Mock Ambulance System...")
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
print("[SUCCESS] Connected to Cloud.\n")

# ==========================================
# 2. HOSPITAL DATABASE (From your Java Code)
# ==========================================
hospitals = {
    "1": {"name": "Sri Ramachandra Hospital", "lat": 13.0381, "lng": 80.1410},
    "2": {"name": "Apollo Hospital", "lat": 13.0633, "lng": 80.2518},
    "3": {"name": "Fortis Malar Hospital", "lat": 13.0067, "lng": 80.2206},
    "4": {"name": "AIIMS", "lat": 28.5672, "lng": 77.2100}
}

print("🏥 Select a Destination Hospital:")
print("1. Sri Ramachandra Hospital")
print("2. Apollo Hospital")
print("3. Fortis Malar Hospital")
print("4. AIIMS")

choice = input("Enter number (1-4): ")
if choice not in hospitals:
    print("Invalid choice, defaulting to Apollo Hospital.")
    choice = "2"

selected_hospital = hospitals[choice]
print(f"\n✅ Selected: {selected_hospital['name']}")

# ==========================================
# 3. STARTING POSITION (Near Guindy)
# ==========================================
current_lat = 13.011500
current_lon = 80.236500
heading = 45.0
driver_name = input("Enter Mock Driver Name (or press Enter for 'Mock Driver'): ")
if not driver_name:
    driver_name = "Mock Driver"

print("\n🚑 Ambulance Engine Started!")
print(f"Driving {driver_name} towards {selected_hospital['name']}... Press Ctrl+C to stop.\n")

try:
    while True:
        payload = {
            'lat': current_lat,
            'lng': current_lon,
            'heading': heading,
            'speed': 60,
            'driverName': driver_name,
            'destination': selected_hospital['name'],
            'destLat': selected_hospital['lat'],
            'destLng': selected_hospital['lng'],
            'timestamp': int(time.time() * 1000),
            'isEmergency': True
        }

        # Push to Firebase
        db.reference('Active_Ambulance/MOCK_AMB_1').set(payload)

        print(f"[LIVE] Pushed: {current_lat:.5f}, {current_lon:.5f} -> {selected_hospital['name']}")

        # Move slightly to simulate driving
        current_lat += 0.0002
        current_lon += 0.0002

        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Mock Ambulance Stopped.")
    db.reference('Active_Ambulance/MOCK_AMB_1').delete()
    print("Database cleared. Safe to exit.")