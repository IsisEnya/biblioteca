from django.apps import AppConfig

class BibliotecaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblioteca'

'''
from django.apps import AppConfig
from django.contrib.auth.models import User

# Consulta para encontrar usuários com um determinado email
users_with_email = User.objects.filter(email='email@example.com')



class BibliotecaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblioteca'
   


    def ready(self):
        from .models import Perfil
        import os
        
        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")
        usuarios = Perfil.objects.filter(email=email)
        if not usuarios: 
            Perfil.objets.create_superuser(username = "admin", email = email, password=senha,
                                            is_active = True, is_staff = True)'''