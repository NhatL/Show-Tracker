from django.shortcuts import render
from django.core.management import call_command

from shows.api import *
# Create your views here.

def index(request):
    call_command("pull_show_details")
    return render(request, "website/index.html")
