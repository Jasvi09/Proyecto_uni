from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from administrator.models import Customer, Business, User
from django_recaptcha.fields import ReCaptchaField

class Customer_Sign_Up_Form(UserCreationForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Customer
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

class Business_Sign_Up_Form(UserCreationForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Business
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

class Log_In_Form(AuthenticationForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('username', 'password', "captcha")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })


class Data_User_Form(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'identification_document','phone_number' )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })
        
        self.fields['last_name'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['identification_document'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })
