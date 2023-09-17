from django.shortcuts import get_object_or_404, render, redirect
from nucleo import settings
from .models import Category, Product, Genero, Perfil
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from pprint import pprint
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def generos(request):
    return {
        'generos': Genero.objects.all()
    }

def categories(request):
    return {
        'categories': Category.objects.all()
    }


def all_products(request):
    products = Product.products.all()
    return render(request, 'biblioteca/home.html', {'products': products})





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



#======================================= PERFIL ====================================================================


def perfil(request, pk):
      
	if request.user.is_authenticated:
		perfil = Perfil.objects.get(usuario_id=pk)
            
		return render(request, "biblioteca/perfil.html", {"perfil":perfil})
	else: 
		messages.success(request, ("Voce tem que logar para acessar essa pagina"))
            
			
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

#============================= CALENDARIO ==========================
'''

def create_google_calendar_event(request):
    # Autenticar com as credenciais do Google
    credentials = service_account.Credentials.from_service_account_info(
    settings.GOOGLE_CALENDAR_CREDENTIALS,
    scopes=['https://www.googleapis.com/auth/calendar']
)

    # Construir o serviço do Google Calendar
    service = build('calendar', 'v3', credentials=credentials)

    # Definir os detalhes do evento
    event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2015-05-28T13:00:00-03:00',  # Data e hora no fuso horário de Brasília
        'timeZone': 'America/Sao_Paulo',  # Fuso horário de Brasília
    },
    'end': {
        'dateTime': '2015-05-28T21:00:00-03:00',  # Data e hora no fuso horário de Brasília
        'timeZone': 'America/Sao_Paulo',  # Fuso horário de Brasília
    },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'isisdagostin19@hotmail.com'},
        {'email': 'isisdagostin@gmail.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    # Inserir o evento no calendário
    event = service.events().insert(calendarId='primary', body=event).execute()
    return HttpResponse(f'Evento criado: {event.get("biblioteca/deucerto.html")}')
'''