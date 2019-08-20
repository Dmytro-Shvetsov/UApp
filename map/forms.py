from django import forms
from .models import Marker
from bootstrap_modal_forms.forms import BSModalForm


class MarkerForm(BSModalForm):
    class Meta:
        model = Marker
        fields = ['name', 'short_description', 'long_description', 'marker_region']

