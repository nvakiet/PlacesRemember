"""place_memories web app URL configurations

The urlpatterns route URL to specific pages in the web app.
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'place_memories'

urlpatterns = [
    path('', views.home, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)