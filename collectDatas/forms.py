from django import forms
from . import models


class MeasuresForm(forms.Form):
    glassware = forms.ChoiceField(label="Select a glassware",
                                  choices=models.GLASSWARE_CHOICE)
    value = forms.FloatField(label="", min_value=0.)


class MeasureForm(forms.ModelForm):

    class Meta:
        model = models.Measure
        fields = ('value',)
        labels = {"value": ""}


class ExperimentForm(forms.ModelForm):

    class Meta:
        model = models.Experiment
        fields = ('name', 'date', 'description')
        labels = {
            "name": "Experiment name",
        }
