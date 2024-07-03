from django import forms
from .models import Object
from django.contrib.auth.models import User

class ObjectPermissionForm(forms.ModelForm):
    permitted_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Object
        fields = ['permitted_users']
