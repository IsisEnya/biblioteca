from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse
from . import views


app_name = 'biblioteca'

urlpatterns = [
    path('', views.all_products, name='todos_livros'),
    path('item/<slug:slug>/', views.detalhe_livro, name='detalhe_livro'),
    path('search/<slug:genero_slug>/', views.lista_genero, name='lista_genero'),
    path('procurar/', views.procurar, name='procurar'),
    path('perfil/<int:pk>/', views.perfil, name='perfil'),
    path('login/', views.login_usuario, name='login'),
    path('logout', views.logout_usuario, name='logout'),
    path('register/', views.register_usuario, name='register'),
    #path('foi/', views.create_google_calendar_event, name='foi'),
    #path('search/', views.pesquisar_livros, name='pesquisar'),
]

