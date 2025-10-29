import os
import json
import requests
from django.conf import settings
from google.oauth2 import service_account
import google.auth.transport.requests
from .models import FCMToken  # Import your model


def send_latest_feed_notification():
    # 1️⃣ Fetch the latest feed
    feed_api = "https://cyberpedia-api-d7x0.onrender.com/notifications/feeds/latest"
    res = requests.get(feed_api)
    if res.status_code != 200:
        print("❌ Failed to fetch latest feed:", res.status_code)
        return

    feed = res.json()
    print("✅ Latest feed fetched:", feed.get("title", "No Title"))

    # 2️⃣ Load Firebase credentials from settings
    if not settings.FIREBASE_CREDENTIALS:
        print("⚠️ FIREBASE_CREDENTIALS not found in settings.")
        return

    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

    try:
        credentials = service_account.Credentials.from_service_account_info(
            settings.FIREBASE_CREDENTIALS,
            scopes=SCOPES
        )
    except Exception as e:
        print("❌ Error loading Firebase credentials:", e)
        return

    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    access_token = credentials.token

    # 3️⃣ Firebase project ID (read dynamically from credentials)
    project_id = settings.FIREBASE_CREDENTIALS.get("project_id", "cyberpediawithflutter")

    # 4️⃣ FCM endpoint
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    # 5️⃣ Fetch all tokens from the database
    tokens = list(FCMToken.objects.values_list('token', flat=True))
    if not tokens:
        print("⚠️ No FCM tokens found in the database.")
        return

    print(f"📦 Sending notification to {len(tokens)} devices...")

    # 6️⃣ Send notification to each token
    for target_token in tokens:
        body = {
            "message": {
                "token": target_token,
                "notification": {
                    "title": feed.get("title", "Cyberpedia Feed Update"),
                    "body": (feed.get("content_snippet") or "")[:200] + "...",
                    "image": feed.get("image", "")
                },
                "android": {
                    "priority": "high",
                    "notification": {
                        "sound": "notification",
                        "channel_id": "high_importance_channel"
                    }
                },
                "apns": {
                    "payload": {"aps": {"sound": "notification.mp3"}}
                },
                "data": {
                    "route": feed.get("screen", "cyber_feeds"),
                    "feed_id": str(feed.get("id", "")),
                },
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))
        print(f"🔔 Sent to {target_token[:8]}... | Status: {response.status_code}")
        if response.status_code != 200:
            print("⚠️ Response:", response.text)

    print("✅ Notification broadcast complete!")
