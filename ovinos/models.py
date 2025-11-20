from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings  

# -------------------------------
# 🐑 Modelo Ovino
# -------------------------------
class Ovino(models.Model):
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    )

    STATUS_CHOICES = (
        ('Disponível', 'Disponível'),
        ('Vendido', 'Vendido'),
        ('Reservado', 'Reservado'),
    )

    numero_brinco = models.CharField(max_length=20, unique=True)
    raca = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cor = models.CharField(max_length=30)
    peso_atual = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    quantidade_crias = models.IntegerField(blank=True, null=True)
    peso_ao_nascer = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    filiacao = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')
    data_nascimento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_ovinos/', blank=True, null=True)

    def __str__(self):
        return f"{self.numero_brinco} - {self.raca}"


class LoteLeilao(models.Model):
    numero_lote = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    data_leilao = models.DateField()
    preco_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='fotos_ovinos/', blank=True, null=True)
    encerrado = models.BooleanField(default=False) 

    def __str__(self):
        return f"Lote {self.numero_lote}"



class Lance(models.Model):
    lote = models.ForeignKey(LoteLeilao, on_delete=models.CASCADE, related_name='lances', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f"Lance de {self.usuario.username} - R$ {self.valor} no {self.lote.numero_lote}"


class Profile(models.Model):
    ROLE_CHOICES = (
        ('organizer','Organizador'),
        ('buyer','Comprador'),
        ('visitor','Visitante'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class AnimalArrematado(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="animais_arrematados"
    )
    lote = models.ForeignKey(LoteLeilao, on_delete=models.CASCADE)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2)
    data_arremate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Lote {self.lote.numero_lote}"

