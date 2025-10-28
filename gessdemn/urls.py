from django.urls import path
from gessdemn.views import (
    get_issues,
    submit_issue,
    display_issues,
    delete_issue,
    HomeView,
    chat_view,         
    chat_endpoint,  
    cromtek_chat_api,  
    save_fcm_token,
    token_list,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('submit-issue/', submit_issue, name='submit_issue'), 
    path('get-issues/', get_issues, name='get_issues'),        
    path('display-issues/', display_issues, name='display_issues'),  
    path('delete-issue/<int:issue_id>/', delete_issue, name='delete_issue'),

    # 👇 New chatbot routes
    path('chat/', chat_view, name='chat'),                 
    path('chatapi/', chat_endpoint, name='chat_endpoint'), 
    path('cromtek_chat_api/',  cromtek_chat_api, name=' cromtek_chat_api'), 
    path('save-fcm/', save_fcm_token, name='save-fcm'),
    path('tokens/', token_list, name='fcm-tokens'),
]
