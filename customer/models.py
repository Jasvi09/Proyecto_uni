from django.db import models
from administrator.models import User

# Create your models here.
order_statuses = (
    ("Pendiente", "Pendiente"),
    ("En proceso", "En proceso"),
    ("Completado", "Completado"),
    ("Cancelado", "Cancelado"),
)

list_formats = (
    ("Rollo Bond x Mt", "Rollo Bond x Mt"),
    ("Lamina Bond", "Lamina Bond"),
    ("Media Lamina Bond", "Media Lamina Bond"),
    ("Tabloide", "Tabloide"),
    ("Oficio", "Oficio"),
    ("Carta", "Carta"),
)

list_types_of_paper = (
    ("Papel Bond", "Papel Bond"),
    ("Papel Glasse", "Papel Glasse"),
    ("Opalina", "Opalina"),
)

list_colors = (
    ("Blanco Y Negro", "Blanco Y Negro"),
    ("Full Color", "Full Color"),
    ("Escala De Grises", "Escala De Grises")
)

class Services_Impression(models.Model):
    name = models.CharField(max_length=255, default="Impresion")
    amount = models.IntegerField(default=1)
    formats = models.CharField(max_length=255, choices=list_formats)
    type_of_paper = models.CharField(max_length=255, choices=list_types_of_paper)
    color = models.CharField(max_length=255,  choices=list_colors)
    others = models.TextField()
    status = models.CharField(max_length=255, choices=order_statuses, default='Pendiente')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_impression')


list_designs = (
    ("Digitalización", "Digitalización"),
    ("Levantamiento", "Levantamiento"),
    ("Adecuación", "Adecuación"),
)

list_architectural_proposals= (
    ("Planos De Arquitectura", "Planos De Arquitectura"),
    ("Diseño Interior", "Diseño Interior"),
    ("Modelacion 3d", "Modelacion 3d"),
    ("Inspección De Obras", "Inspección De Obras"),
)

class Services_Arquitecture(models.Model):
    name = models.CharField(max_length=255, default="Arquitectura")
    desing = models.CharField(max_length=255,  choices=list_designs)
    architectural_proposal = models.CharField(max_length=255,  choices=list_architectural_proposals)
    others = models.TextField()
    status = models.CharField(max_length=255, choices=order_statuses, default='Pendiente')
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_arquitecture')