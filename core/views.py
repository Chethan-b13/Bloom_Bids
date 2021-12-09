from typing import Generic
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class Homepage(TemplateView):
    template_name = "index.html"
