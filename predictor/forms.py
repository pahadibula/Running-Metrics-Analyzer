# predictor/forms.py

from django import forms

class RunInputForm(forms.Form):
    distance = forms.FloatField(label='Distance (km)', min_value=0.1)
    minutes = forms.IntegerField(label='Minutes', min_value=0)
    seconds = forms.IntegerField(label='Seconds', min_value=0, max_value=59)
