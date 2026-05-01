import firebase_admin
from firebase_admin import credentials, messaging

# 1. Setup (Use your same JSON file)
cred = credentials.Certificate("serviceAccount.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# 2. Target the topic you subscribed to in LoginActivity
topic = "lane_a" 

# 3. Create the DATA payload
message = messaging.Message(
    data={
        "title": "🚨 TEST ALERT",
        "body": "Ambulance coming! This is a 82-line code test.",
        "lat": "12.8406",
        "lng": "80.1534"
    },
    topic=topic,
)

# 4. Send!
response = messaging.send(message)
print("Successfully sent message:", response)