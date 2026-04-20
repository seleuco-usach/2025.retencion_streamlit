from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Persona

def personas_view(request):
    if request.method == 'POST':
        Persona.objects.create(
            nombre=request.POST['nombre'],
            edad=request.POST['edad']
        )
        return redirect('personas')

    personas = Persona.objects.all()
    return render(request, 'personas/personas.html', {
        'personas': personas
    })
