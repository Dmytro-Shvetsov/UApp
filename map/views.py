from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Region
from .utils import preprocess
from uapp.settings import BASE_DIR
from django.urls import reverse_lazy
from .forms import MarkerForm
from .models import Marker, MarkerEstimator
from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.decorators import login_required
from django.conf import settings


def index(request):
    regions_info_filepath = f'{BASE_DIR}/map/templates/ukraine.kml'
    regions_info = preprocess.preprocess_coords(regions_info_filepath)
    marker = Marker.objects.all()
    context = {
        'regions_info': regions_info,
        'markers': marker
    }
    return render(request, 'map/index.html', context)


class MarkerCreateView(BSModalCreateView):
    template_name = 'map/create-marker.html'
    form_class = MarkerForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    success_message = 'Success: Marker was created.'
    success_url = reverse_lazy('Home')


def marker_info_view(request):
    if request.method == 'GET':
        marker_id = request.GET.get('marker_id')
        marker_obj = Marker.objects.get(pk=marker_id)
        estimator = MarkerEstimator.objects.get_or_create(user=request.user, marker=marker_obj)[0]
        context = {
            'marker': marker_obj,
            'estimator': estimator
        }
        return render(request, 'map/helpers/marker_information.html', context)

    return HttpResponseForbidden('Allowed only via GET')


def estimate_marker_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    'user_is_logged': 'no'
                })

        marker_id = request.POST.get('marker_id')
        marker = Marker.objects.get(pk=marker_id)
        vote = request.POST.get('vote')

        estimator = MarkerEstimator.objects.get_or_create(user=request.user, marker=marker)[0]
        estimator.vote = vote

        estimator.save(update_fields=['vote'])
        return JsonResponse({
            'user_is_logged': 'yes',
            'like_count': marker.get_likes_count(),
            'dislike_count': marker.get_dislikes_count()
        })
