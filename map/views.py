from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Region
from .utils import preprocess
from uapp.settings import BASE_DIR
from django.urls import reverse_lazy
from .forms import MarkerForm
from .models import Marker
from bootstrap_modal_forms.generic import BSModalCreateView

def index(request):
    regions_info_filepath = f'{BASE_DIR}/map/templates/ukraine.kml'
    regions_info = preprocess.preprocess_coords(regions_info_filepath)
    marker = Marker.objects.all()
    context = {
        'regions_info': regions_info,
        'markers': marker
    }
    return render(request, 'index.html', context)


class MarkerCreateView(BSModalCreateView):
    template_name = 'create-marker.html'
    form_class = MarkerForm
    success_message = 'Success: Marker was created.'
    success_url = reverse_lazy('Home')

