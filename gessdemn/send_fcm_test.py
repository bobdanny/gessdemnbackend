from google.oauth2 import service_account
import requests
import json
import google.auth.transport.requests

def send_v1_notification():
    # Define scope and credentials
    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
    SERVICE_ACCOUNT_FILE = 'firebase_key.json'  # path to your downloaded JSON key

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    access_token = credentials.token

    # Your Firebase project ID
    project_id = "cyberpediawithflutter"

    # Firebase API endpoint
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    # Request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    # Request body
    body = {
        "message": {
            "token": "f3d6NYNaRfiVRWfmSG9Vv6:APA91bFzyqpj2a9LDBwgmfnQFVekOjgK3n3TPJLC1GHh3z6LH1lyhqpQvxvfc-JifIbiSjhUcflEBmzDlvb4d7h7pBC5kJ3RhZ_d0HDzQLVo1RcC7-kUeac",
            "notification": {
                "title": "🔥 Test from Django (FCM V1)",
                "body": "This message was sent using your Firebase Admin key!"
            },
            "android": {
                "priority": "high"
            }
        }
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(body))

    print("Status:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    send_v1_notification()
