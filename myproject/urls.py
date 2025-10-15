from django.contrib import admin
from django.urls import path, include
from gessdemn.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gessdemn/', include('gessdemn.urls')),
    path('', HomeView.as_view(), name='home'),
]
