"""This module contains the views of place_memories web app.
"""
from django.shortcuts import render
from django.views.generic import ListView
from .models import UserMemories
from django.contrib.postgres.search import SearchVector
from urllib.parse import unquote

# Create your views here.
def home(requests):
    """Render the homepage of the app.
    """
    return render(requests, "place_memories/home.html")

class UserMemoriesView(ListView):
    model = UserMemories
    paginate_by = 5
    template_name = "place_memories/user_memories.html"
    ordering = "placename"

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", None)
        if ordering:
            fieldname, order = ordering.split("_")
            if order == "desc":
                ordering = "-" + fieldname
            else:
                ordering = fieldname
        else:
            ordering = "placename"
        return ordering
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(user_id=self.request.user.id)
        # If the query parameter has "search", use postgresql to do text search
        search_value = self.request.GET.get("search", None)
        if search_value:
            search_value = unquote(str(search_value))
            queryset = queryset.annotate(
                search=SearchVector("placename", "address", "comment")
            ).filter(search=search_value)
        return queryset