from django.db import models

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
