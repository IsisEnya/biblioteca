from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Category, Product, Genero, Perfil
from django.contrib.auth.models import AbstractUser

#DELETANDO UMA COISINHAS
admin.site.unregister(Group)

#----------------------------
'''admin.site.register(User,UserAdmin)

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["nome_usuario"]'''

class Perfiljunto(admin.StackedInline):
    model = Perfil
    

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "email"]
    inlines = [Perfiljunto]

admin.site.unregister(User)

admin.site.register(User,UserAdmin)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'slug', 'quantidade',
                    'no_estoque', 'criado', 'updated','reserva','editora','genero','data_publicacao','codigo_livro']
    list_filter = ['no_estoque', 'disponivel']
    list_editable = ['quantidade', 'no_estoque']
    prepopulated_fields = {'slug': ('titulo',)}

    

#-----CODIGO FUNCIONANDO--------------
'''from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'slug', 'quantidade',
                    'no_estoque', 'criado', 'updated']
    list_filter = ['no_estoque', 'disponivel']
    list_editable = ['quantidade', 'no_estoque']
    prepopulated_fields = {'slug': ('titulo',)}

    '''