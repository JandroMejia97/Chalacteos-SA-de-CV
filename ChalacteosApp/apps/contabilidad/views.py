from django.shortcuts import render

# Create your views here.

def Cuentas(request):
	return render(request, 'contabilidad/cuentas.html',{})

