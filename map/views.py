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
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


def index(request):
    regions_info_filepath = f'{BASE_DIR}/map/templates/ukraine.kml'
    regions_with_cords = preprocess.preprocess_coords(regions_info_filepath)
    context = {
        'regions': regions_with_cords
    }
    return render(request, 'index.html', context)


class MarkerCreateView(BSModalCreateView):
    template_name = 'create-marker.html'
    form_class = MarkerForm
    success_message = 'Success: Marker was created.'
    success_url = reverse_lazy('Home')


    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         print("loh")
    #         form = MarkerForm(request.POST)
    #         if form.is_valid():
    #             name = request.POST.get('name', '')
    #             short_description = request.POST.get('short_description', '')
    #             long_description = request.POST.get('long_description', '')
    #             longitude = request.POST.get('longitude', '')
    #             latitude = request.POST.get('latitude', '')
    #             marker_region = request.POST.get('marker_region', '')
    #             # marker_region_obj = Region(name=marker_region)
    #             print("loh1")
    #             marker_obj_reg = Region.objects.all().values('name' == 'marker_region')
    #
    #             marker_obj = Marker(name=name, short_description=short_description, long_description=long_description,
    #                                 longitude=longitude, latitude=latitude, marker_region=marker_obj_reg)
    #             marker_obj.save()
    #             print("loh1")
    #         return redirect('Home')


