from django.forms import ModelForm
from .models import Services_Arquitecture, Services_Impression
from django_recaptcha.fields import ReCaptchaField

class Service_impression_Form(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Services_Impression
        fields = ["amount","formats", "type_of_paper", "color", "others"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['formats'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['type_of_paper'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['color'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['others'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['others'].required = False

class Service_architecture_Form(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Services_Arquitecture
        fields = ["desing","architectural_proposal", "others"]

    def  __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['desing'].widget.attrs.update({
             'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['architectural_proposal'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['others'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

        self.fields['others'].required = False
