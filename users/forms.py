from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import UserSetting

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'is_staff'] 

class UserSettingsForm(ModelForm):
    class Meta:
        model = UserSetting
        fields = [ 'ttl' ]

        ttl = forms.NumberInput()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #self.helper.form_action = reverse_lazy('users:view_profile')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit','Submit'))
        
        self.fields['ttl'].label = 'Time to live (in clicks).'
