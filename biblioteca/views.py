from django.shortcuts import get_object_or_404, render, redirect
from nucleo import settings
from .models import Category, Product, Genero, Perfil
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm,ProductForm, CategoryForm, GeneroForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from pprint import pprint
import datetime
import os.path
from django import forms
from django.http import HttpResponseRedirect
from plyer import notification
import time
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.wsgi import get_wsgi_application
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
application = get_wsgi_application()

#------------------------------------------------------------------------------------------------------------------------------------------------





from win10toast import ToastNotifier

def notify_me(title, message, image_path=None):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10, threaded=True, icon_path=image_path)


def generos(request):
    return {
        'generos': Genero.objects.all()
    }

def categories(request):
    return {
        'categories': Category.objects.all()
    }

#============================================================= CALENDARIO ==========================================================================================


def calendario(request):
    



    return render(request, 'biblioteca/home.html')

#==================================================== TODOS OS PRODUTOS ===============================================================


def all_products(request):
    products = Product.objects.all().order_by('titulo')

    data_limite = timezone.now() - timedelta(days=3)

    # Obtenha todos os produtos que foram adicionados à reserva há mais de 3 dias
    produtos_expirados = Product.objects.filter(data_reserva__lt=data_limite)

    # Remova esses produtos da reserva
    for produto in produtos_expirados:
        produto.adicionar_reserva.clear() 

    return render(request, 'biblioteca/home.html', {'products': products})


#====================================================================================================================================================


def lista_categoria(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'biblioteca/category.html', {'category': category, 'products': products})




def lista_genero(request, genero_slug=None):
    genero = get_object_or_404(Genero, slug=genero_slug)
    products = Product.objects.filter(genero=genero)
    return render(request, 'biblioteca/genero.html', {'genero': genero, 'products': products})




def detalhe_livro(request, slug):
    product = get_object_or_404(Product, slug=slug, no_estoque=True)
    return render(request, 'biblioteca/detalhes.html', {'product': product})



def procurar(request):
    if request.method == "POST":
        searched = request.POST['searched'] 
        filtro = request.POST['filtro']
        
        if filtro == 'titulo':
            livros = Product.objects.filter(titulo__icontains=searched)
        elif filtro == 'genero':
            livros = Product.objects.filter(autor__icontains=searched)
        elif filtro == 'autor':
            livros = Product.objects.filter(editora__icontains=searched)
        elif filtro == 'data':
            livros = Product.objects.filter(data_publicacao__icontains=searched)
        else:
            # Caso não haja um filtro válido selecionado, retorne todos os livros
            livros = Product.objects.all()
            
        return render(request, 'biblioteca/procurar.html', {'searched': searched, 'livros': livros, 'filtro': filtro})
    else:
        return render(request, 'biblioteca/procurar.html', {})

#====================================== LISTA DE DESEJO FUNÇAO ===========================================
@login_required
def adicionar_desejo(request, id):
    product = get_object_or_404(Product, id=id)
    if product.lista_desejos.filter(id = request.user.id).exists():
          product.lista_desejos.remove(request.user)
    else:
          product.lista_desejos.add(request.user)   
          notify_me("Produto Adicionado à Lista de Desejos", f"Você adicionou {product.titulo} à sua lista de desejos.","logoroxa.png")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


#============================================== RESERVA SÓ ==================================================

@login_required
def adicionar_reserva(request, id):
    product = get_object_or_404(Product, id=id)

    # Verifique se o usuário já adicionou o produto à reserva
    if product.adicionar_reserva.filter(id=request.user.id).exists():
        # Se sim, remova-o da reserva
        product.adicionar_reserva.remove(request.user)
        
    else:
        # Se não, adicione-o à reserva e defina a data de adição
        product.adicionar_reserva.add(request.user)
        product.data_reserva = timezone.now()
        product.save()

        # Notifique o usuário sobre a adição à reserva
        notify_me("Produto Adicionado à Lista de reserva", f"Você adicionou {product.titulo} à sua lista de reserva.","logoroxa.png")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

#============================================== RESERVA COM GOOGLE ==================================================

@login_required
def adicionar_reserva_calendario(request, id):
    product = get_object_or_404(Product, id=id)

    # Verifique se o usuário já adicionou o produto à reserva
    if product.adicionar_reserva.filter(id=request.user.id).exists():
        # Se sim, remova-o da reserva
        product.adicionar_reserva.remove(request.user)
        
    else:
        # Se não, adicione-o à reserva e defina a data de adição
        product.adicionar_reserva.add(request.user)
        product.data_reserva = timezone.now()
        product.save()
        

        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file("client_secret_100551806101-gj6e3lqlqgd34n4cn7c5s1jb1u8itbch.apps.googleusercontent.com.json", scopes=scopes)
        credentials = flow.run_local_server(host='localhost', port=8080, authorization_prompt_message='Please visit this URL to authorize this application: {url}', success_message='A autenticação foi concluída com sucesso. Você pode fechar esta janela.', open_browser=True)
        pickle.dump(credentials, open("token.pkl", "wb"))
        credentials = pickle.load(open("token.pkl", "rb"))
        service = build("calendar", "v3", credentials=credentials)


        result = service.calendarList().list().execute()
        result['items'][0]

        calendar_id = result['items'][0]['id']
        result = service.events().list(calendarId=calendar_id, timeZone="America/Belem").execute()
        result['items'][0]

        

        # Definindo start_time para daqui a 3 dias
        start_time = datetime.now() + timedelta(days=3)
        end_time = start_time + timedelta(hours=4)
        timezone_str = 'America/Belem'

        event = {
            'summary': f'Reserva do livro {product.titulo}',
            'location': 'Satc',
            'description': 'Esse é o último dia para você poder retirar o livro de sua biblioteca local!',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone_str,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone_str,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        service.events().insert(calendarId=calendar_id, body=event).execute()
            

        # Notifique o usuário sobre a adição à reserva
        notify_me("Produto Adicionado à Lista de reserva", f"Você adicionou {product.titulo} à sua lista de reserva.","logoroxa.png")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

#============================================= PERFIL ====================================================================



def perfil(request, perfil_id):
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(id=perfil_id)
        #reserva = Product.objects.filter(reserva=request.user)
        lista_desejos = Product.objects.filter(lista_desejos=request.user)
        return render(request, "biblioteca/perfil.html", {"perfil": perfil, 'lista_desejos': lista_desejos,})
    else:
        messages.success(request, ("Você tem que estar logado para acessar esta página"))
        return render(request, 'biblioteca/home.html', {})
      
    


#============================== LOGIN E LOGOUT ===================

def login_usuario(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		usuario = authenticate(request, username=username, password=password)
	

		if usuario is not None:
				login(request, usuario)
                
				messages.success(request, "You Have Been Logged In! Get MEEPING!")

				return redirect('biblioteca:todos_livros')  # Replace with your actual URL name
		else:
				messages.success(request, "There was an error logging in. Please Try Again...")
                
				return render(request, "biblioteca/login.html", {})
	else:
			return render(request, "biblioteca/login.html", {})

def logout_usuario(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out. Sorry to See You Go...")
    return redirect('biblioteca:todos_livros')

#==================================== REGISTER USUARIO ========================================= #

def register_usuario(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			email = form.cleaned_data['email']
			# Log in user
			usuario = authenticate(username=username, password=password, email=email)
			login(request,usuario)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return render(request, 'biblioteca/home.html', {})
	
	return render(request, "biblioteca/register.html", {'form':form})



#======================= VER LISTA DE DESEJO ===============================#



#------------------------------------------------------------------------------------------

def criar_produto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
    else:
        form = ProductForm()


    return render(request, 'biblioteca/criar_produto.html', {'form': form})

#------------------------------------------------------------------------------------------------
def criar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
    else:
        form = GeneroForm()


    return render(request, 'biblioteca/criar_genero.html', {'form': form})


#-------------------------------------------------------------------------------------------------------

def criar_categoria(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
    else:
        form = CategoryForm()


    return render(request, 'biblioteca/criar_catego.html', {'form': form})

#-------------------------------------------------------------------------------------------------------

def adm(request):

    return render(request, 'biblioteca/adm.html')