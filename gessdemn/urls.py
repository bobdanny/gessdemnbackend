from django.urls import path
from gessdemn.views import (
    get_issues,
    submit_issue,
    display_issues,
    delete_issue,
    HomeView,
    chat_view,         # 👈 added
    chat_endpoint,     # 👈 added (for API use)
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('submit-issue/', submit_issue, name='submit_issue'), 
    path('get-issues/', get_issues, name='get_issues'),        
    path('display-issues/', display_issues, name='display_issues'),  
    path('delete-issue/<int:issue_id>/', delete_issue, name='delete_issue'),

    # 👇 New chatbot routes
    path('chat/', chat_view, name='chat'),                 # For HTML chat page
    path('chatapi/', chat_endpoint, name='chat_endpoint'), # Optional JSON chat API
]
