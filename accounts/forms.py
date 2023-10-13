from django import forms
from .models import * 


class registerationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class':'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
        'class':'form-control',
    }))
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'mobile_number']
        extra_fields = ['password','confirm_password']

    def __init__(self, *args, **kwargs):
        super(registerationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['mobile_number'].widget.attrs['placeholder'] = 'Enter your mobile number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

class profileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False,error_messages={'invalid':{'images file only'}},widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'mobile_number','profile_image','address_line_1', 'address_line_2','city', 'state', 'country']

    def __init__(self,*args,**kwargs):
        super(profileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'