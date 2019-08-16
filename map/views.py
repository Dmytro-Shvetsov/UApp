from django.shortcuts import render
from django.http import HttpResponse
from .models import Region
from .utils import preprocess
from uapp.settings import BASE_DIR


def index(request):
    reg = Region.objects.get(pk=1)
    regions_info_filepath = f'{BASE_DIR}/map/templates/ukraine.kml'
    regions_with_cords = preprocess.preprocess_coords(regions_info_filepath)
    context = {
        'reg': reg,
        'regions': regions_with_cords
    }
    return render(request, 'index.html', context)


