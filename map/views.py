from django.shortcuts import render
from django.http import HttpResponse
from .models import Region

def index(request):
    reg = Region.objects.get(pk=1)
    context = {
        'reg': reg
    }
    return render(request, 'index.html', context)