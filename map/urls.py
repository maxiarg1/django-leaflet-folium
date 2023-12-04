from django.urls import path
from .views import home, actualizar_marcadores

urlpatterns = [
    path('', home, name='home'),
    path('actualizar_marcadores/', actualizar_marcadores, name='actualizar_marcadores'),  # Corrige la ruta
]