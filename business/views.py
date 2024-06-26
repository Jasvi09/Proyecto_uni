from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse

from django_recaptcha.client import submit
from django_recaptcha.fields import ReCaptchaField



from administrator.models import Business, Profile, User
from administrator.form import Business_Sign_Up_Form, Data_User_Form, Log_In_Form
from administrator.tokens import account_activation_token

from customer.models import Services_Arquitecture, Services_Impression

from .models import Services
from .form import ServiceForm, ServiceUpdateForm

# Create your views here.

def dashboard(request):
    if request.method == 'GET':
        try:
            order_pending_arqui = Services_Arquitecture.objects.filter(status="Pendiente")
            order_pending_impri = Services_Impression.objects.filter(status="Pendiente")
            if order_pending_arqui.exists() or order_pending_impri.exists() :
                order_pending  = True
            else:
                order_pending  = False
                
            return render(request, "dashboard_business.html", {
                "order_pending": order_pending
            }) 
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "dashboard_business.html")
        
def my_services(request):
    if request.method == 'GET':
        try:
            my_services = Services.objects.filter(user=request.user)
            return render(request, "my_services_business.html", {
                'services': my_services
            }) 
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "my_services_business.html")

def update_my_services(request, service_id):
    if request.method == "GET":
        try: 
            service = get_object_or_404(Services, pk=service_id, user=request.user)
            form = ServiceUpdateForm(instance=service)
            return render(request, "update_my_services_business.html", {
                "service": service,
                "form": form,
            })
        except:
            service = get_object_or_404(Services, pk=service_id, user=request.user)
            form = ServiceUpdateForm(instance=service)
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "update_my_services_business.html", {
                "service": service,
                "form": form,
            })
    elif request.method == "POST":
        try: 
            service = get_object_or_404(Services, pk=service_id, user=request.user)
            form = ServiceUpdateForm(request.POST, instance=service)
            if form.is_valid:
                form.save()
                messages.success(request, "Actualizado el servicio.")
                return redirect('my_services_business')
            else:
                service = get_object_or_404(Services, pk=service_id, user=request.user)
                form = ServiceUpdateForm(request.POST, instance=service)
                messages.error(request, "Ha ocurrido un error.")
                return render(request, "update_my_services_business.html", {
                "service": service,
                "form": form,
            })
        except:
            service = get_object_or_404(Services, pk=service_id, user=request.user)
            form = ServiceUpdateForm(request.POST, instance=service)
            messages.error(request, "Ha ocurrido un error")
            return render(request, "update_my_services_business.html", {
                "service": service,
                "form": form,
            })

def add_my_services(request):
    if request.method == "GET":
        try:
            form = ServiceForm()
            return render(request, "add_my_services_business.html", {
                "form": form
            })
        except:
            form = ServiceForm()
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "add_my_services_business.html", {
                "form": form,
            })
    elif request.method == "POST":
        try: 
            data = ServiceForm(request.POST)
            service = request.POST["name"]
            exist = Services.objects.filter(name=service, user=request.user).exists()
            if exist == True:
                form = ServiceForm()
                messages.error(request, "Ya existe el servicio.")
                return render(request, "add_my_services_business.html", {
                    "form": form,
                })
            else:
                if data.is_valid:
                    form = data.save(commit=False)
                    form.user = request.user
                    form.is_active = True
                    form.save()
                    messages.success(request, "Añadido el servicio.")
                    return redirect('my_services_business')
                else:
                    form = ServiceForm()
                    messages.error(request, "Ha ocurrido un errorr.")
                    return render(request, "add_my_services_business.html", {
                        "form": form,
                    })
        except:
            form = ServiceForm()
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "add_my_services_business.html", {
                "form": form,
            })

def delete_my_services(request, service_id):
    if request.method == "POST":
        try:
            service = get_object_or_404(Services, pk=service_id, user=request.user)
            service.delete()
            messages.success(request, "Eliminado el servicio.")
            return redirect("my_services_business")
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "my_services")

def orders(request):
    if request.method == 'GET':
        try:
            orders = [Services_Impression.objects.all(), Services_Arquitecture.objects.all()]
            return render(request, 'orders_business.html', {
                'impresiones': orders[0][::-1],
                'arquitecturas': orders[1][::-1],
            })
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "orders_business.html")

def completed_orders(request, service_type, order_id):
    if request.method == 'GET':
        try:
            if service_type == 'Impresión':
                impri = get_object_or_404(Services_Impression, pk=order_id)
                impri.status = 'Completado'
                impri.save()
                messages.success(request, f"Se ha completado la orden de impresión #{order_id}.")
                return redirect('orders_business')
            
            if service_type == 'Arquitectura':
                arqui = get_object_or_404(Services_Arquitecture, pk=order_id)
                arqui.status = 'Completado'
                arqui.save()
                messages.success(request, f"Se ha completado la orden de arquitectura #{order_id}.")
                return redirect('orders_business')
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, 'orders_business.html')

def accept_orders(request, service_type, order_id):
    if request.method == 'GET':
        try:
            if service_type == 'Impresión':
                impri = get_object_or_404(Services_Impression, pk=order_id)
                impri.status = 'En proceso'
                impri.save()
                messages.success(request, f"Se ha aceptado la orden de impresión #{order_id}.")
                return redirect('orders_business')
            
            if service_type == 'Arquitectura':
                arqui = get_object_or_404(Services_Arquitecture, pk=order_id)
                arqui.status = 'En proceso'
                arqui.save()
                messages.success(request, f"Se ha aceptado la orden de arquitectura #{order_id}.")
                return redirect('orders_business')
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, 'orders_business.html')

def cancel_orders(request, service_type,order_id):
    if request.method == 'GET':
        try:
            if service_type == 'Impresión':
                impri = get_object_or_404(Services_Impression, pk=order_id)
                impri.status = 'Cancelado'
                impri.save()
                messages.success(request, f"Se ha cancelado la orden de impresión #{order_id}.")
                return redirect('orders_business')
            
            if service_type == 'Arquitectura':
                arqui = get_object_or_404(Services_Arquitecture, pk=order_id)
                arqui.status = 'Cancelado'
                arqui.save()
                messages.success(request, f"Se ha cancelado la orden de arquitectura #{order_id}.")
                return redirect('orders_business')
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, 'orders_business.html')

def log_in(request):
    if request.method == "GET":
        try:
            return render(request, "log_in_business.html", {
                'form': Log_In_Form
            })
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "log_in_business.html", {
                'form': Log_In_Form
            })
    elif request.method == "POST":
        
        try:
            form =  Log_In_Form(request.POST)
            if form.is_valid:
                username = request.POST["username"]
                password = request.POST["password"]
            else:
                messages.error(request, "Ha ocurrido un error.")
                return render(request, "log_in_business.html", {
                    'form': Log_In_Form
                })
        except: 
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "log_in_business.html", {
                'form': Log_In_Form
            })

        try:
            business = Business.objects.get(username=username)
            if business.role != 'BUSINESS':
                messages.error(request, "No tiene permiso de business.")
                return render(request, "log_in_business.html", {
                    'form': Log_In_Form
                })
        except Business.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            return render(request, "log_in_business.html", {
                'form': Log_In_Form
            })

        try:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Usuario o contraseña incorrecta.")
                return render(request, "log_in_business.html", {
                    'form': Log_In_Form
                })
            else:
                
                ip_c = ReCaptchaField.get_remote_ip(request)
                recaptcha_response = submit(request.POST.get('g-recaptcha-response'), '6LdeIfkpAAAAAEL6BWrZ0ZZj92bn8JC8OhYam6P9', ip_c)
                
                if recaptcha_response.is_valid:
                    login(request, user)
                    messages.success(request, "Haz iniciado sesión.")
                    return redirect("dashboard_business")                
                else:
                    messages.error(request, "Verificación de CAPTCHA fallida.")
                    return render(request, "log_in_business.html", {
                        "form": Log_In_Form(request.POST)
                    })
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "log_in_business.html", {
                'form': Log_In_Form
            })

def sign_up(request):
    if request.method == "GET":
        try:
            return render(request, "sign_up_business.html", {
                'form': Business_Sign_Up_Form
            })
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "sign_up_business.html", {
                'form': Business_Sign_Up_Form,
            })
    elif request.method == "POST":
            form = Business_Sign_Up_Form(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                auth_token = account_activation_token.make_token(user=user)
                profile = Profile.objects.create(user=user, auth_token=auth_token, is_verified=False)
                profile.save()
                domain = get_current_site(request).domain
                send_mail_after_registration(user.username, user.email, profile.auth_token, domain)
                login(request, user)
                messages.success(request, "Registro exitoso.")
                print("aqui")
                return redirect("verify_profile_business")
                # service_id = request.session.get('service_id')
                # if service_id:
                #     return redirect('add_orders_business', service_id=service_id)
            else:
                messages.error(request, "Ha ocurrido un error al crear la cuenta. Por favor, verifica los datos ingresados.")
                return render(request, "sign_up_business.html", {
                    'form': Business_Sign_Up_Form
                })          

def log_out(request):
    if  request.method == "GET":
        try:
            messages.success(request, "Haz cerrado sesión")
            logout(request)
            return redirect("log_in_business")
        except:
             messages.error(request, "Ha ocurrido un error.")
             return redirect("dashboard_business")

def verify_account(request, auth_token):
    try:
        profile_obj = get_object_or_404(Profile, auth_token=auth_token, user= request.user)
        if profile_obj:
            if profile_obj.is_verified == True and profile_obj.data_full == False:
                return redirect("verify_profile_business")
            elif profile_obj.is_verified == True and profile_obj.data_full == True:
                return redirect("verify_profile_business")
            
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Email activado exitosamente.")
            return redirect("verify_profile_business")
        else:
            messages.success(request, "No se a podido validar el email.")
            return redirect("verify_profile_business")
    except:
        messages.success(request, "No se a podido validar el email.")
        return redirect("verify_profile_business")

def verify_profile(request):
    if request.method == "GET":
        try:
            profile = get_object_or_404(Profile, user=request.user)
            if profile.is_verified == False:
                messages.info(request, f"Revisa tu correo electronico {request.user.email}, y presiona el link de activación.") 
                return render(request, "verify_profile_business.html", {
                    'email': False
                })

            if profile.data_full == False:
                messages.info(request, "Completa el registro.") 
                return render(request, "verify_profile_business.html", {
                    'data': False,
                    'form': Data_User_Form
                })

            if profile.is_verified == True and profile.data_full == True:
                messages.success(request, "Cuenta ya activa.")
                return render(request, "verify_profile_business.html", {
                    'verifid': True,
                    'redireccionar': True,
                })
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "verify_profile_business.html", {
                'form': Data_User_Form
            })
    elif request.method == "POST":
        try:
            a = User.objects.get(pk=request.user.id)
            form = Data_User_Form(request.POST, instance=a)
            if form.is_valid():
                form.save()
                profile = get_object_or_404(Profile, user=request.user)
                profile.data_full = True
                profile.save()
                messages.success(request, "Se ha guardado los datos.")
                return redirect("verify_profile_business")
            else:
                messages.error(request, "Ha ocurrido un error.")
                return render(request, "verify_profile_business.html", {
                    "form": form,
                })        
        except:
            messages.error(request, "Ha ocurrido un error.")
            return render(request, "verify_profile_business.html", {
                "form": form,
            })    

def send_mail_after_registration(username, to_email, token, domain, view_name='verify_account_business'):
    subject = f'Tu cuenta necesita ser verificada {username}.'
    verify_url = domain + reverse(view_name, kwargs={'auth_token':token})
    message = f'Hola {username}, presiona este link para verificar tu cuenta {verify_url}'
    email = EmailMessage(subject, message, to=[to_email])
    email.send()