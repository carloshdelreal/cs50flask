from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ( AuthenticationForm, UserCreationForm )

class LoginForm (AuthenticationForm):
    AuthenticationForm.base_fields['username'].widget.attrs.update({'class': "form-control"})
    AuthenticationForm.base_fields['password'].widget.attrs.update({'class': "form-control"})
    class Meta:
        model = User
        fields = [ 'username', 'password']