from django.shortcuts import render
from django.views.generic import ListView
from .models import Event

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter().order_by("-date")[:10]
        return context
