import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.db import migrations
import sys
from nucleo import settings

from django.db import models



#======================================= LIVROS =============================================


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(disponivel=True)

#===================================== CATEGORIA ============================================

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)


    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('biblioteca:lista_categoria', args=[self.slug])

    def __str__(self):
        return self.name
    
#====================================== GENERO ==========================================

class Genero(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'generos'

    def get_absolute_url(self):
        return reverse('biblioteca:lista_genero', args=[self.slug])

    def __str__(self):
        return self.name
    
#================================== O LIVRO EM SI ====================================


class Product(models.Model):
    categoria = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    genero = models.ManyToManyField(Genero)
    codigo_livro = models.CharField(max_length=255, default= 'adimin')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, default='admin')
    editora = models.CharField(max_length=255, default='admin')
    descricao = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    quantidade = models.IntegerField(default=1)
    no_estoque = models.BooleanField(default=True)
    disponivel = models.BooleanField(default=True)
    criado = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()
    data_publicacao = models.DateField(default=datetime.date.today)
    lista_desejos = models.ManyToManyField(User, related_name="lista_desejos", blank=True)

    

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-criado',)

    def get_absolute_url(self):
        return reverse('biblioteca:detalhe_livro', args=[self.slug])

    def __str__(self):
        return self.titulo
    
    
#======================================= USUARIO / PERFIL ======================================================================================================  

class Perfil(models.Model):
    lista_desejos = models.ManyToManyField(Product, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username


    def criar_perfil(sender, instance, created, **kwargs):
        if created:
            user_profile = Perfil(usuario =instance)
            user_profile.save()
            user_profile.save()

    post_save.connect(criar_perfil, sender=User)

    #=============================================================





    #==================umas esplicações pra estudo===============
'''    class Meta: Essa é uma classe interna em um modelo Django. Ela é usada para configurar metadados específicos do modelo. Neste caso, duas configurações estão sendo feitas:

verbose_name_plural: Define o nome plural para o modelo. Em vez de usar o nome padrão com um "s" no final (por exemplo, "Productss"), esse atributo definirá o nome como "Products".
ordering: Especifica a ordenação padrão para consultas do banco de dados. Aqui, está sendo definido que os objetos do modelo Product devem ser ordenados pelo campo criado em ordem decrescente (mais recente primeiro).
def get_absolute_url(self): Este é um método definido no modelo. Ele é usado para retornar a URL absoluta para o objeto atual (self). No exemplo, a URL absoluta é gerada usando a função reverse, que é uma função utilitária do Django para construir URLs com base em um nome de URL registrado e quaisquer argumentos necessários. A URL retornada será para a visualização de detalhes de um produto no aplicativo biblioteca (requisitando a view detalhe_livro), com um argumento passado na URL correspondente ao campo slug do produto atual.

def __str__(self): Esse método especial é chamado quando uma representação em string do objeto precisa ser retornada. Neste caso, ele retorna o valor do campo titulo do objeto Product. Isso é útil para fornecer uma representação legível do objeto quando ele é exibido, por exemplo, na interface de administração do Django ou em depuração.'''
    
