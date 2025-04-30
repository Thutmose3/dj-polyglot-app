from django import forms

from .models import SourceProject


class SourceProjectForm(forms.ModelForm):
    """Form for SourceProject."""

    class Meta:
        model = SourceProject
        fields = ["name"]
