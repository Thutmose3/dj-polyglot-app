from .models import SourceProject
from django import forms

from django.contrib.auth.models import User


class SourceProjectForm(forms.ModelForm):
    """Form for SourceProject."""

    class Meta:
        model = SourceProject
        fields = ["name"]
