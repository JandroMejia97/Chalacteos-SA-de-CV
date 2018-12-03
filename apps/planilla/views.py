from django.shortcuts import render

# Create your views here.

def import_data_departamento(request):
	f = 'C:\\departamentos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			empresa=new[1]
			nombre=new[2]
			descripcion=new[3]
			objeto, created = Departamento.objects.update_or_create(
				empresa=empresa,
				nombre=nombre,
				descripcion=descripcion
			)
	return HttpResponse('Hecho')

def import_data_puesto(request):
	f = 'C:\\puestos.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			departamento=new[1]
			codigo_puesto=new[2]
			nombre_funcional=new[3]
			descripcion=new[4]
			salario_base=new[5]
			objeto, created = Puesto.objects.update_or_create(
				departamento=departamento,
				codigo_puesto=codigo_puesto,
				nombre_funcional=nombre_funcional,
				descripcion=descripcion,
				departamento=departamento,
				salario_base=salario_base,
			)
	return HttpResponse('Hecho')

def import_data_empleado(request):
	f = 'C:\\empleados.csv'
	with open(f) as file:
		reader = csv.reader(file)
		for new in reader:
			row=new[0].split(";")
			puesto=new[1]
			dui=new[2]
			fecha_nacimiento=new[3]
			telefono=new[4]
			direccion=new[5]
			is_active=new[6]
			objeto, created = Empleado.objects.update_or_create(
				puesto=puesto,
				dui=dui,
				fecha_nacimiento=fecha_nacimiento,
				telefono=telefono,
				direccion=direccion,
				is_active=is_active,
			)
	return HttpResponse('Hecho')