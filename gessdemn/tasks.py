import openai
from django.conf import settings
from .models import Issue

openai.api_key = settings.OPENAI_API_KEY

def fetch_ai_priority_and_response(issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        
        prompt = f"""
You are a helpful customer support AI assistant.

1. Analyze the following issue and determine its priority: Low, Medium, or High.
2. Provide a short, human-like response or advice for the customer, written naturally like a human would say it.

Issue: "{issue.issue}"

Format your response like this:

Priority: <Low/Medium/High>
Suggestion: <Your natural human-like reply>
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  
            max_tokens=200
        )

        ai_text = response.choices[0].message.content.strip()

        priority = "Low"
        suggestion = ai_text

        if "Priority:" in ai_text:
            lines = ai_text.splitlines()
            for line in lines:
                if line.startswith("Priority:"):
                    priority_candidate = line.split("Priority:")[1].strip()
                    if priority_candidate in ["Low", "Medium", "High"]:
                        priority = priority_candidate
                if line.startswith("Suggestion:"):
                    suggestion = line.split("Suggestion:")[1].strip()

        issue.priority = priority
        issue.ai_suggestion = suggestion
        issue.ai_status = 'Completed'
        issue.save()

        print(f"Issue ID {issue.id} updated: Priority={priority}, Suggestion={suggestion}")

    except Issue.DoesNotExist:
        print(f"Issue ID {issue_id} does not exist.")
    except Exception as e:
        print(f"Error processing issue ID {issue_id}: {e}")











from apscheduler.schedulers.background import BackgroundScheduler
from .services import send_latest_feed_notification

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_latest_feed_notification, 'interval', seconds=30)
    scheduler.start()
    print("⏱️ Scheduler started: sending feed notifications every 30s")
