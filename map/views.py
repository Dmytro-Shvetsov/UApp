from django.shortcuts import render
from django.http import HttpResponse
from .models import Region
from .utils import preprocess
from uapp.settings import BASE_DIR


def index(request):
    regions_info_filepath = f'{BASE_DIR}/map/templates/ukraine.kml'
    regions_info = preprocess.preprocess_coords(regions_info_filepath)

    context = {
        'regions_info': regions_info
    }
    return render(request, 'index.html', context)


