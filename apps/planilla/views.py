from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse 
import csv

from django.views.generic.list import ListView

from django.urls import reverse_lazy

from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required

from .forms import *

from django.template import  RequestContext

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView

)
# Create your views here.

def index(request):
    return render(request,"inicio/index.html")

class EmpresaDetail(DetailView):
    model = Empresa
    template_name="planilla/empresa/empresa_detail.html"

class EmpresaList(ListView):
    model = Empresa
    template_name ="planilla/empresa/empresa_list.html"
    paginate_by = 10

class EmpresaCreation(CreateView):
    model = Empresa
    success_url = reverse_lazy('appsic:list')
    template_name ="planilla/empresa/empresa_form.html"
    form_class = EmpresaForm

class EmpresaUpdate(UpdateView):
    model = Empresa
    success_url = reverse_lazy('appsic:list')
    template_name ="planilla/Empresa/empresa_form.html"
    form_class = EmpresaForm

class EmpresaDelete(DeleteView):
    model = Empresa
    success_url = reverse_lazy('appsic:list')
    template_name = "planilla/empresa/empresa_confirm_delete.html"

#Empleados

class EmpleadoList(ListView):
    model = Empleado
    template_name ="planilla/empleado/empleado_list.html"
    paginate_by = 10

class EmpleadoDetail(DetailView):
    model = Empleado
    template_name="planilla/empleado/empleado_detail.html"


class EmpleadoCreation(CreateView):
    model = Empleado
    success_url = reverse_lazy('appsic:list_empleado')
    template_name ="planilla/empleado/empleado_form.html"
    form_class = EmpleadoForm

class EmpleadoUpdate(UpdateView):
    model = Empleado
    success_url = reverse_lazy('appsic:list_empleado')
    template_name ="planilla/empleado/empleado_form.html"
    form_class = EmpleadoForm

class EmpleadoDelete(DeleteView):
    model = Empleado
    success_url = reverse_lazy('appsic:list_empleado')
    template_name = "planilla/empleado/empleado_confirm_delete.html"


#Departamento
class DepartamentoList(ListView):
    model = Departamento
    template_name ="planilla/departamento/departamento_list.html"
    paginate_by = 10


class DepartamentoDetail(DetailView):
    model = Departamento
    template_name="planilla/departamento/departamento_detail.html"


class DepartamentoCreation(CreateView):
    model = Departamento
    success_url = reverse_lazy('appsic:list_departamento')
    template_name ="planilla/departamento/departamento_form.html"
    form_class = DepartamentoForm

class DepartamentoUpdate(UpdateView):
    model = Departamento
    success_url = reverse_lazy('appsic:list_departamento')
    template_name ="planilla/departamento/departamento_form.html"
    form_class = DepartamentoForm

class DepartamentoDelete(DeleteView):
    model = Departamento
    success_url = reverse_lazy('appsic:list_departamento')
    template_name = "planilla/departamento/departamento_confirm_delete.html"


#Puesto
class PuestoList(ListView):
    model = Puesto
    template_name ="planilla/puesto/puesto_list.html"
    paginate_by = 10


class PuestoDetail(DetailView):
    model = Puesto
    template_name="planilla/puesto/puesto_detail.html"


class PuestoCreation(CreateView):
    model = Puesto
    success_url = reverse_lazy('appsic:list_puesto')
    template_name ="planilla/puesto/puesto_form.html"
    form_class = PuestoForm

class PuestoUpdate(UpdateView):
    model = Puesto
    success_url = reverse_lazy('appsic:list_puesto')
    template_name ="planilla/puesto/puesto_form.html"
    form_class = PuestoForm

class PuestoDelete(DeleteView):
    model = Puesto
    success_url = reverse_lazy('appsic:list_puesto')
    template_name = "planilla/puesto/puesto_confirm_delete.html"



#Empleado - Empresa


class EmpleadoEmpresaList(ListView):
    model = EmpleadoEmpresa
    template_name ="planilla/empleado_empresa/empleadoempresa_list.html"
    paginate_by = 10


class EmpleadoEmpresaDetail(DetailView):
    model = EmpleadoEmpresa
    template_name="planilla/empleado_empresa/empleadoempresa_detail.html"


class EmpleadoEmpresaCreation(CreateView):
    model = EmpleadoEmpresa
    success_url = reverse_lazy('appsic:list_empleadoempresa')
    fields = ['id', 'empleado', 'empresa']
    template_name ="planilla/empleado_empresa/empleadoempresa_form.html"

class EmpleadoEmpresaUpdate(UpdateView):
    model = EmpleadoEmpresa
    success_url = reverse_lazy('appsic:list_empleadoempresa')
    fields = ['id', 'empleado', 'empresa']
    template_name ="planilla/empleado_empresa/empleadoempresa_form.html"

class EmpleadoEmpresaDelete(DeleteView):
    model = EmpleadoEmpresa
    success_url = reverse_lazy('appsic:list_empleadoempresa')
    template_name = "planilla/empleado_empresa/empleadoempresa_confirm_delete.html" 



#Puesto - Empresa

class PuestoEmpresaList(ListView):
    model = PuestoEmpresa
    template_name ="planilla/puesto_empresa/puestoempresa_list.html"
    paginate_by = 10


class PuestoEmpresaDetail(DetailView):
    model = PuestoEmpresa
    template_name="planilla/puesto_empresa/puestoempresa_detail.html"


class PuestoEmpresaCreation(CreateView):
    model = PuestoEmpresa
    success_url = reverse_lazy('appsic:list_puestoempresa')
    fields = ['id', 'puesto', 'empresa']
    template_name ="planilla/puesto_empresa/puestoempresa_form.html"

class PuestoEmpresaUpdate(UpdateView):
    model = PuestoEmpresa
    success_url = reverse_lazy('appsic:list_puestoempresa')
    fields = ['id', 'puesto', 'empresa']
    template_name ="planilla/puesto_empresa/puestoempresa_form.html"

class PuestoEmpresaDelete(DeleteView):
    model = PuestoEmpresa
    success_url = reverse_lazy('appsic:list_puestoempresa')
    template_name = "planilla/puesto_empresa/puestoempresa_confirm_delete.html" 




#Departamento - Empresa

class DepartamentoEmpresaList(ListView):
    model = DepartamentoEmpresa
    template_name ="planilla/departamento_empresa/departamentoempresa_list.html"
    paginate_by = 10


class DepartamentoEmpresaDetail(DetailView):
    model = DepartamentoEmpresa
    template_name="planilla/departamento_empresa/departamentoempresa_detail.html"


class DepartamentoEmpresaCreation(CreateView):
    model = DepartamentoEmpresa
    success_url = reverse_lazy('appsic:list_departamentoempresa')
    fields = ['id', 'departamento', 'empresa']
    template_name ="planilla/departamento_empresa/departamentoempresa_form.html"

class DepartamentoEmpresaUpdate(UpdateView):
    model = DepartamentoEmpresa
    success_url = reverse_lazy('appsic:list_departamentoempresa')
    fields = ['id', 'departamento', 'empresa']
    template_name ="planilla/departamento_empresa/departamentoempresa_form.html"

class DepartamentoEmpresaDelete(DeleteView):
    model = DepartamentoEmpresa
    success_url = reverse_lazy('appsic:list_departamentoempresa')
    template_name = "planilla/departamento_empresa/departamentoempresa_confirm_delete.html" 

#Asignación

class AsignacionList(ListView):
    model = Asignacion
    template_name ="planilla/asignacion/asignacion_list.html"
    paginate_by = 8


class Empresa_AsignacionList(ListView):
    model = Empresa
    template_name ="planilla/Empresa/empresas_list.html"
    paginate_by = 8



class AsfilterList(ListView):
    model = Empresa
    template_name ="planilla/asignacion/asfilter.html"
    paginate_by = 8

def Asignaciones(request,pk):
    empresa = Empresa.objects.get(id=pk)
    #emp = EmpleadoEmpresa.objects.get(empresa=empresa)
    asignaciones = Asignacion.objects.filter(empleado_empresa__empresa = empresa)
    return render(request, 'planilla/asignacion/asignacion_listar.html', {'asignaciones':asignaciones})



def asignacion(request,pk):

    empleados = EmpleadoEmpresa.objects.filter(empresa_id=pk)
    puestos = PuestoEmpresa.objects.filter(empresa_id=pk)
    departamentos = DepartamentoEmpresa.objects.filter(empresa_id=pk)

    if request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            asignacion = Asignacion(empleado_empresa = form.cleaned_data['empleado_empresa'],
                puesto_empresa = form.cleaned_data['puesto_empresa'], departamento_empresa = form.cleaned_data['departamento_empresa'],
                salario_asignado = form.cleaned_data['salario_asignado'], fecha_asignacion = form.cleaned_data['fecha_asignacion'], 
                calendario = form.cleaned_data['calendario'])
            asignacion.save()
            return redirect('appsic:asignacion_listar', pk)
        else:
            return render(request, 'planilla/asignacion/asignacion.html',{'form':form,
                'empleados':empleados, 'puestos':puestos, 'departamentos':departamentos}) 
            #, context_instance = RequestContext(request)
    else:
        form = AsignacionForm
    return render(request, 'planilla/asignacion/asignacion.html',{'form':form,
     'empleados':empleados, 'puestos':puestos, 'departamentos':departamentos})


def asignacion_editar(request,pk):

    asignacion = get_object_or_404(Asignacion, pk = pk)

    emp = asignacion.empleado_empresa.empresa

    empleados = EmpleadoEmpresa.objects.filter(empresa=emp)
    puestos = PuestoEmpresa.objects.filter(empresa=emp)
    departamentos = DepartamentoEmpresa.objects.filter(empresa=emp)

    if request.method == 'POST':
        form = AsignacionForm(request.POST, instance = asignacion)
        if form.is_valid():
            asignacion.save()
            return redirect('appsic:list')
        else:
            return render(request, 'planilla/asignacion/asignacion.html',{'form':form,
                'empleados':empleados, 'puestos':puestos, 'departamentos':departamentos}, 
                context_instance = RequestContext(request))
    else:
        form = AsignacionForm(instance=asignacion)
    return render(request, 'planilla/asignacion/asignacion.html',{'form':form,
     'empleados':empleados, 'puestos':puestos, 'departamentos':departamentos})
    #, context_instance = RequestContext(request)

class AsignacionDelete(DeleteView):
    model = Asignacion
    success_url = reverse_lazy('appsic:list_asignacion')
    template_name = "planilla/asignacion/asignacion_confirm_delete.html"

#Renta
class RentaList(ListView):
    model = Renta 
    template_name ="planilla/renta/renta_list.html"

class RentaCreation(CreateView):
    model = Renta 
    success_url = reverse_lazy('appsic:list_renta')
    fields = ['id', 'tipo', 'v1','v2','porc']
    template_name ="planilla/renta/renta_form.html"

class RentaUpdate(UpdateView):
    model = Renta 
    success_url = reverse_lazy('appsic:list_renta')
    fields = ['id', 'tipo', 'v1','v2','porc']
    template_name ="planilla/renta/renta_form.html"

class PlanillaDelete(DeleteView):
    model = DetallePlanilla 
    success_url = reverse_lazy('appsic:filtro')
    template_name = "planilla/apps/planilla_confirm_delete.html"



def consultar_planillas(request):

    planillas= DetallePlanilla.objects.all()

    return render(request, 'planilla/apps/consultar_planillas.html',{'planillas':planillas})


def consultar_empresa(request):
    empresas = Empresa.objects.all()
    return render(request, 'planilla/apps/consultar.html',{'empresas': empresas}) 


def buscar(request):
   
    errors = [] 
    if 'q' in request.GET: 
        q = request.GET['q'] 
        if not q: 
          errors.append('Por favor introduce un termino de busqueda')

        else:
            empresa = Empresa.objects.get(nombre=q)
            empleado_empresa = EmpleadoEmpresa.objects.filter(empresa=empresa) 
            #asignacion = Asignacion.objects.filter(empleado_empresa=empleado_empresa) 
            return render(request, 'planilla/apps/newPlanillas.html',{'empleado_empresa': empleado_empresa}) 
 
    return render(request, 'planilla/apps/consultar.html', {'errors': errors})

def filtro(request):
    errors = [] 
    if 'q' in request.GET: 
        q = request.GET['q'] 
        if not q: 
          errors.append('Por favor introduce un termino de busqueda')
    if 'ee' in request.GET:
        ee = request.GET['ee']
        if not ee: 
          errors.append('Por favor introduce un termino de busqueda')

        else:
            empresa = Empresa.objects.get(nombre=ee)
            planillas = DetallePlanilla.objects.filter(fecha=q, empresa=empresa)
            ee = empresa.ncr

            total1 = 0
            total2 = 0
            total3 = 0
            total4 = 0
            for al in planillas :
                total1 = float(total1) + float(al.pago_real)
                total2 = float(total2) + float(al.isss_patronal)
                total3 = float(total3) + float(al.afp_patronal)
                total4 = float(total4) + float(al.vacaciones)

            total = total1 + total2 + total3 + total4
            total = "{0:.2f}".format(float(total))


            return render(request, 'planilla/apps/filtro_planillas.html',{'planillas': planillas,'total1': total1, 'total2': total2
                , 'total3': total3, 'total4': total4, 'total': total, 'ee':ee}) 

    empresas = Empresa.objects.all()
 
    return render(request, 'planilla/apps/consultar_fecha.html', {'errors': errors, 'empresas':empresas }) 


def newPlanilla(request):
    if request.method=='POST':
        if request.POST['hdnAccion']=='insertar':
            #nic = Empresa.objects.get(nic=request.POST['nic'])
            #nombre = Empresa.objects.get(nombre=request.POST['nombre'])
            #ncr = Empresa.objects.get(ncr=request.POST['ncr'])
            emp_emp = EmpleadoEmpresa.objects.get(id=request.POST['ee'])


            descuentos = request.POST['descuentos']
            ingresos = request.POST['ingresos']

            descuentos = float(descuentos)
            ingresos = float(ingresos)

            asignacion=Asignacion.objects.get(empleado_empresa=emp_emp)  ###get filter
            sn = asignacion.salario_asignado
            sp = sn
            cb = asignacion.calendario
            snd = sn/cb
            dias_trabajados = request.POST['dias']
            snv = float(snd)*float(dias_trabajados) 

            isss_empleado = snv*0.03
            isss_patronal = snv*0.075
            afp_empleado = snv*0.0625
            afp_patronal = snv*0.0675
            
            renta1 = Renta.objects.get(id=1)
            renta2 = Renta.objects.get(id=2)
            renta3 = Renta.objects.get(id=3)
            renta4 = Renta.objects.get(id=4)
            renta5 = Renta.objects.get(id=5)
            renta6 = Renta.objects.get(id=6)
            renta7 = Renta.objects.get(id=7)
            renta8 = Renta.objects.get(id=8)
            renta9 = Renta.objects.get(id=9)
            renta10 = Renta.objects.get(id=10)
            renta11 = Renta.objects.get(id=11)
            renta12 = Renta.objects.get(id=12)


            #Salario Semanal
            if(cb>0 and cb<=7):
                if(snv>=renta9.v1):
                    renta = (float(snv) - float(renta9.v1))*float(renta9.porc)
                if(snv>=renta10.v1):
                    renta = (float(snv) - float(renta10.v1))*float(renta10.porc)
                if(snv>=renta11.v1):
                    renta = (float(snv) - float(renta11.v1))*float(renta11.porc)
                if(snv>=renta12.v1):
                    renta = (float(snv) - float(renta12.v1))*float(renta12.porc)
                vacaciones = (float(snd)*float(15) + float(snd)*float(15)*0.30 + float(snd)*float(15)*0.1425)/float(52)

            #Quincenal
            if(cb>=8 and cb<=15):
                if(snv>=renta5.v1):
                    renta = (float(snv) - float(renta5.v1))*float(renta5.porc)
                if(snv>=renta6.v1):
                    renta = (float(snv) - float(renta6.v1))*float(renta6.porc)
                if(snv>=renta7.v1):
                    renta = (float(snv) - float(renta7.v1))*float(renta7.porc)
                if(snv>=renta8.v1):
                    renta = (float(snv) - float(renta8.v1))*float(renta8.porc)
                vacaciones = (float(snd)*float(15) + float(snd)*float(15)*0.30 + float(snd)*float(15)*0.1425)/float(26)

            #Mensual
            if(cb>=16 and cb<=30):
                if(snv>=renta1.v1):
                    renta = (float(snv) - float(renta1.v1))*float(renta1.porc)
                if(snv>=renta2.v1):
                    renta = (float(snv) - float(renta2.v1))*float(renta2.porc)
                if(snv>=renta3.v1):
                    renta = (float(snv) - float(renta3.v1))*float(renta3.porc)
                if(snv>=renta4.v1):
                    renta = (float(snv) - float(renta4.v1))*float(renta4.porc)
                vacaciones = (float(snd)*float(15) + float(snd)*float(15)*0.30 + float(snd)*float(15)*0.1425)/float(12)


    


            aguinaldo = float(snd)*float(18)
            

            salario_neto = snv - isss_empleado - afp_empleado - renta - descuentos + ingresos
            pago_real = snv + isss_patronal + afp_patronal + aguinaldo + vacaciones



            planilla = DetallePlanilla()
            planilla.fecha = request.POST['fecha']
            planilla.asignacion = asignacion
            planilla.empresa = emp_emp.empresa
            planilla.dias_trabajados = request.POST['dias']
            planilla.descuentos = request.POST['descuentos']
            planilla.ingresos = request.POST['ingresos']
            planilla.isss_empleado=isss_empleado
            planilla.isss_patronal=isss_patronal
            planilla.afp_empleado=afp_empleado
            planilla.afp_patronal=afp_patronal
            planilla.renta=renta
            planilla.aguinaldo=sp
            planilla.vacaciones=vacaciones
            planilla.salario_neto=salario_neto
            planilla.pago_real=snv
            planilla.save()

            return render(request, "planilla/apps/newPlanillas.html")
    return render(request, "planilla/apps/newPlanillas.html")




def pasajeros_problematicos_csv(request,pk):
    planilla = DetallePlanilla.objects.get(id=pk)
    fecha = planilla.fecha
    empresa = planilla.empresa
    
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename=planilla.csv'
    pl2 = DetallePlanilla.objects.filter(fecha=fecha,empresa=empresa)
    

    writer = csv.writer(response)
    writer.writerow(['No.','Fecha Nombre Apellido Puesto Dias ISSS AFP Renta Salario'])
    for (year, num) in zip(range(1, 100), pl2):
        writer.writerow([year,num])
    return response
