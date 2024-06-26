from django.forms import ModelForm
from .models import Services
from django_recaptcha.fields import ReCaptchaField

class ServiceForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Services
        fields = ["name"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'w-full mt-2 px-3 py-2 text-gray-500 bg-transparent outline-none border focus:border-indigo-600 shadow-sm rounded-lg'
        })

class ServiceUpdateForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Services
        fields = ["is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['is_active'].widget.attrs.update({
            'class': 'relative flex w-5 h-5 bg-white peer-checked:bg-indigo-600 rounded-md border ring-offset-2 ring-indigo-600 duration-150 peer-active:ring cursor-pointer after:absolute after:inset-x-0 after:top-[3px] after:m-auto after:w-1.5 after:h-2.5 after:border-r-2 after:border-b-2 after:border-white after:rotate-45'
        })
