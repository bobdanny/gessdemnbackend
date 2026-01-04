from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Issue
from .tasks import fetch_ai_priority_and_response  
from django.views.generic import TemplateView



@csrf_exempt
def submit_issue(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            issue_text = data.get('issue')

            if not all([name, email, issue_text]):
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

            issue = Issue.objects.create(name=name, email=email, issue=issue_text)

            try:
                fetch_ai_priority_and_response(issue.id)
            except Exception as e:
                print("AI task error:", e)

            return JsonResponse({'status': 'success', 'message': 'Issue submitted! AI response should appear shortly.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)


def get_issues(request):
    if request.method == 'GET':
        issues = Issue.objects.all().order_by('-submitted_at')
        data = [
            {
                'id': issue.id,
                'name': issue.name,
                'email': issue.email,
                'issue': issue.issue,
                'priority': issue.priority or "Pending",
                'ai_suggestion': issue.ai_suggestion or "",
                'submitted_at': issue.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for issue in issues
        ]
        return JsonResponse({'status': 'success', 'issues': data}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Only GET method is allowed'}, status=405)


def display_issues(request):
    issues = Issue.objects.all().order_by('-submitted_at')
    return render(request, 'issues_list.html', {'issues': issues})

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.all().order_by('-submitted_at')
        return context


    
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_issue(request, issue_id):
    try:
        issue = get_object_or_404(Issue, id=issue_id)
        issue.delete()
        return JsonResponse({'status': 'success', 'message': 'Issue deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



















from django.shortcuts import render
from .chatbot_tasks import chat_with_ai
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_view(request):
    """
    Renders a simple HTML page for chatting with the AI.
    Handles user input and displays AI response.
    """
    ai_reply = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.POST.get("message", "")
        if user_message:
            ai_reply = chat_with_ai(user_message)

    return render(request, "chat.html", {
        "user_message": user_message,
        "ai_reply": ai_reply
    })





































from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .gizmotize import gizmotize

@csrf_exempt
def gizmotize(request):
    """
    API endpoint for gizmotize AI chat.
    Accepts POST requests with a JSON body: { "message": "user message" }
    Returns JSON: { "status": "success", "reply": "AI response" }
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            if not user_message:
                return JsonResponse({"status": "error", "message": "Message cannot be empty"}, status=400)

            ai_response = chat_with_cromtek(user_message)
            return JsonResponse({"status": "success", "reply": ai_response}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST method allowed"}, status=405)
























from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FCMToken

@api_view(['POST'])
def save_fcm_token(request):
    token = request.data.get('token')
    device_name = request.data.get('device_name', 'Unknown')

    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    obj, created = FCMToken.objects.get_or_create(token=token, defaults={'device_name': device_name})
    if not created:
        obj.device_name = device_name
        obj.save()

    return Response({'message': 'Token saved successfully!'}, status=status.HTTP_200_OK)






from django.shortcuts import render
from django.core.paginator import Paginator
from .models import FCMToken

def token_list(request):
    qs = FCMToken.objects.order_by('-created_at')
    paginator = Paginator(qs, 20)  # 20 tokens per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'token_list.html', {'page_obj': page_obj})











from django.http import JsonResponse
from .services import send_latest_feed_notification

def trigger_feed_notification(request):
    send_latest_feed_notification()
    return JsonResponse({"message": "Notification sent manually!"})
