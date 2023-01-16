"""This module contains the views of place_memories web app.
"""
from django.shortcuts import render

# Create your views here.
def home(requests):
    """Render the homepage of the app.
    """
    return render(requests, "place_memories/home.html")
