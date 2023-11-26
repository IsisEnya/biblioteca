from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404



app_name = 'biblioteca'

urlpatterns = [
   
    path('', views.all_products, name='todos_livros'),
    path('item/<slug:slug>/', views.detalhe_livro, name='detalhe_livro'),
    path('search/<slug:genero_slug>/', views.lista_genero, name='lista_genero'),
    path('procurar/', views.procurar, name='procurar'),
    path('perfil/<int:perfil_id>/', views.perfil, name='perfil'),
    path('accounts/login/', views.login_usuario, name='login'),
    path('logout', views.logout_usuario, name='logout'),
    path('register/', views.register_usuario, name='register'),
    path('criar-produto/', views.criar_produto, name='criar_produto'),
    path('criar-genero/', views.criar_genero, name='criar_genero'),
    path('criar-categoria/', views.criar_categoria, name='criar_categoria'),
    path('adm/', views.adm, name='adm'),
    path('lista-de-desejos/adicionar/<int:id>/', views.adicionar_desejo, name='adicionar_desejo'),
    path('adiciona-reserva/adicionar/<int:id>/', views.adicionar_reserva, name='adicionar_reserva'),
    path('adicionar-reserva-calendario/adicionar/<int:id>/', views.adicionar_reserva_calendario, name='adicionar_reserva_calendario'),
]
   


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

