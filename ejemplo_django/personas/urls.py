from django.urls import path
from .views import personas_view

urlpatterns = [
    path('', personas_view, name='personas'),
]
