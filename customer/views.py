from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from business.models import Services
from administrator.models import Customer, Profile, User
from .form import Service_impression_Form, Service_architecture_Form
from administrator.form import Customer_Sign_Up_Form, Data_User_Form, Log_In_Form
from django.contrib.sites.shortcuts import get_current_site
from administrator.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
import time
from .models import Services_Impression, Services_Arquitecture

# Create your views here.


def index(request):
    if request.method == 'GET':
        try:
            return render(request, "index.html")
        except:
            return render(request, "index.html", {
                'error': 'a ocurrido un error'
            })


def dashboard(request):
    if request.method == 'GET':
        try:
            return render(request, "dashboard_customer.html")
        except:
            return render(request, "dashboard_customer.html", {
                'error': 'a ocurrido un error'
            })


def services(request):
    if request.method == 'GET':
        try:
            services = Services.objects.all()
            return render(request, "services_customer.html", {
                'services': services
            })
        except:
            return render(request, "services_customer.html", {
                'error': 'a ocurrido un error'
            })
    elif request.method == 'POST':
        try:
            return render(request, "services_customer.html")
        except:
            return render(request, "services_customer.html", {
                'error': 'a ocurrido un error'
            })


def add_orders(request, service_type, service_id):
    if request.method == 'GET':
        try:
            service = get_object_or_404(Services, pk=service_id, name=service_type)
            if service.name == 'Impresión':
                form = Service_impression_Form()
                return render(request, "add_orders_customer.html", {
                    'form_impri': form,
                    'services': service
                })
            if service.name == 'Arquitectura':
                form = Service_architecture_Form()
                return render(request, "add_orders_customer.html", {
                    'form_arqui': form,
                    'services': service
                })
        except:
            return render(request, "add_orders_customer.html", {
                'error': 'a ocurrido un error'
            })
    elif request.method == 'POST':
        try:
            service = get_object_or_404(Services, pk=service_id, name=service_type)
            if service.name == 'Impresión':
                data = Service_impression_Form(request.POST)
                form = data.save(commit=False)
                form.user = request.user
                form.name = service.name
                form.save()
                return redirect('services_customer')

            if service.name == 'Arquitectura':
                
                data = Service_architecture_Form(request.POST)
                form = data.save(commit=False)
                form.user = request.user
                form.name = service.name
                form.save()
                return redirect('services_customer')

        except:
            return render(request, "add_orders_customer.html", {
                'form': data,
                'error': 'a ocurrido un error'
            })


def my_orders(request):
    if request.method == 'GET':
        try:

            orders = [Services_Impression.objects.filter(user=request.user), Services_Arquitecture.objects.filter(user=request.user)]
            return render(request, 'my_orders_customer.html', {
                'impresiones': orders[0][::-1],
                'arquitecturas': orders[1][::-1],
            })
        except:
            return render(request, "my_orders_customer.html", {
                'impresiones': orders[0][::-1],
                'arquitecturas': orders[1][::-1],
                'error': 'a ocurrido un error'
            })

def cancel_orders(request, service_type,order_id):
    if request.method == 'GET':
        try:
            if service_type == 'Impresión':
                impri = get_object_or_404(Services_Impression, pk=order_id)
                impri.status = 'Cancelado'
                impri.save()
                return redirect('my_orders_customer')
            
            if service_type == 'Arquitectura':
                arqui = get_object_or_404(Services_Arquitecture, pk=order_id)
                arqui.status = 'Cancelado'
                arqui.save()
                return redirect('my_orders_customer')
        except:
            return render(request, 'my_orders_customer.html',{
                'error': 'a ocurrido un error'
            })


def log_in(request):
    if request.method == "GET":
        try:
            return render(request, "log_in_customer.html", {
                'form': Log_In_Form
            })
        except:
            return render(request, "log_in_customer.html", {
                'error': "a ocurrido un error",
                'form': Log_In_Form
            })
    elif request.method == "POST":

        form =  Log_In_Form(request.POST)
        if form.is_valid:
            username = request.POST["username"]
            password = request.POST["password"]

        try:
            customer = Customer.objects.get(username=username)
            if customer.role != 'CUSTOMER':
                return render(request, "log_in_customer.html", {
                    'error': "No tiene permiso de customer",
                    'form': Log_In_Form
                })
        except Customer.DoesNotExist:
            return render(request, "log_in_customer.html", {
                'error': "El usuario no existe",
                'form': Log_In_Form
            })

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "log_in_customer.html", {
                'error': "Usuario o contraseña incorrecta",
                'form': Log_In_Form
            })
        else:
            login(request, user)
            return redirect("dashboard_customer")


def seleccionar_pedido(request, service_id):
    request.session['pedido_id'] = service_id
    return redirect('sign_up_customer')


def sign_up(request):
    if request.method == "GET":
        try:
            return render(request, "sign_up_customer.html", {
                'form': Customer_Sign_Up_Form
            })
        except:
            return render(request, "sign_up_customer.html", {
                'form': Customer_Sign_Up_Form,
                'error': "a ocurrido un error",
            })
    elif request.method == "POST":
        form = Customer_Sign_Up_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            auth_token = account_activation_token.make_token(user=user)
            profile = Profile.objects.create(
                user=user, auth_token=auth_token, is_verified=False)
            profile.save()
            domain = get_current_site(request).domain
            send_mail_after_registration(
                user.username, user.email, profile.auth_token, domain)
            login(request, user)
            return render (request, "verify_profile_customer.html", {"msj": "Se ha enviado un correo de verificación"})
            # service_id = request.session.get('service_id')
            # if service_id:
            #     return redirect('add_orders_customer', service_id=service_id)

        else:
            return render(request, "sign_up_customer.html", {"form": form, "error": "Formulario inválido"})


def log_out(request):
    logout(request)
    return redirect("log_in_customer")



def verify_account(request, auth_token):
    try:
        profile_obj = get_object_or_404(Profile, auth_token=auth_token, user= request.user)
        if profile_obj:
            if profile_obj.is_verified == True and profile_obj.data_full == False:
                return redirect("verify_profile_customer")
            elif profile_obj.is_verified == True and profile_obj.data_full == True:
                return redirect("verify_profile_customer")
            
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Email activada exitosamente.")
            return redirect("verify_profile_customer")
        else:
            messages.success(request, "no se a podido validar el email")
            return redirect("verify_profile_customer")
    except Exception as e:
        messages.success(request, "no se a podido validar el email")
        return redirect("verify_profile_customer")


def verify_profile(request):
    if request.method == "GET":
        try:
            profile = get_object_or_404(Profile, user=request.user)
            
            if profile.is_verified == False:
                messages.info(request, f"Revisa tu correo electronico {request.user.email}, y presiona el link de activación") 
                return render(request, "verify_profile_customer.html", {
                    'email': False
                    })

            if profile.data_full == False:
                messages.info(request, "Completa el registro") 
                return render(request, "verify_profile_customer.html", {
                    'data': False,
                    'form': Data_User_Form
                })

            if profile.is_verified == True and profile.data_full == True:
                print("aa")
                messages.success(request, "Cuenta ya activa")
                return render(request, "verify_profile_customer.html", {
                    'verifid': True,
                    'redireccionar': True,
                    })

        except:
            return render(request, "verify_profile_customer.html", {
                "error": "a ocurrido un error",
                'form': Data_User_Form
            })
    elif request.method == "POST":
        a = User.objects.get(pk=request.user.id)
        form = Data_User_Form(request.POST, instance=a)
        if form.is_valid():
            form.save()
            profile = get_object_or_404(Profile, user=request.user)
            profile.data_full = True
            profile.save()
            return redirect("verify_profile_customer")
        else:
            return render(request, "verify_profile_customer.html", {"form": form, "error": "Formulario inválido"})

def send_mail_after_registration(username, to_email, token, domain, view_name='verify_account_customer'):
    subject = 'Tu cuenta necesita ser verificada'
    verify_url = domain + reverse(view_name, kwargs={'auth_token':token})
    print(verify_url)
    message = f'Hola {username}, presiona este link para verificar tu cuenta {verify_url}'
    email = EmailMessage(subject, message, to=[to_email])
    email.send()