from django import forms
from django.forms import ModelForm

from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import SharedSecret


class SharedSecretForm(ModelForm):
    class Meta:
        model = SharedSecret
        fields = ['name', 'text', 'ttl']
        #fields = '__all__'
        #name = forms.CharField()
        #test = forms.Textarea(attrs={'maxlength':250})

        ttl = forms.NumberInput()
        widgets = {
            'text': forms.Textarea(attrs={'maxlength':250}),
        } 
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('secrets:secret_add')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit','Submit'))
        

        self.fields['ttl'].label = 'Time to live (in clicks).'
        self.fields['text'].label = 'Text to encrypt.  Max 250 characters'

        #for name, field in self.fields.items():
        #    field.widget.attrs.update({'class': 'input'})
            