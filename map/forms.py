from django import forms
from .models import Marker
from bootstrap_modal_forms.forms import BSModalForm


class MarkerForm(BSModalForm):
    class Meta:
        model = Marker
        fields = ['name', 'description', 'longitude', 'latitude', 'marker_region']
