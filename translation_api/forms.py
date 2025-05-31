from django import forms

from .models import SourceProject


class SourceProjectForm(forms.ModelForm):

    class Meta:
        model = SourceProject
        fields = ["name"]
