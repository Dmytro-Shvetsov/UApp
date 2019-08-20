from django import forms
from .models import Marker
from bootstrap_modal_forms.forms import BSModalForm

# class MarkerCreation(forms.Form):
#     name = forms.CharField(label='Name of problem', max_length=30)
#     short_description = forms.char(label='Give us a short description', max_length=200)
#     long_description = forms.char(label='Long description', max_length=500)


class MarkerForm(BSModalForm):
    class Meta:
        model = Marker
        fields = ['name', 'short_description', 'long_description', 'marker_region', 'longitude', 'latitude']

