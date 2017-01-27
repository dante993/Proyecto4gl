# -*- encoding: utf-8 -*-
from django.shortcuts import render
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle,Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.contrib.auth.hashers import make_password
from django.template import loader, context,RequestContext
from django.http import *
from LibSoft.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from .forms import *
import string
from random import choice
from datetime import datetime
import csv
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

# Create your views here.

def GenPasswd(n):
    return ''.join([choice(string.letters + string.digits) for i in range(n)])


def v_home(request):
    mi_template = loader.get_template("home.html")
    return HttpResponse(mi_template.render())

def man1(request):
    mi_template = loader.get_template("manual/m1.html")
    return HttpResponse(mi_template.render())
def man2(request):
    mi_template = loader.get_template("manual/m2.html")
    return HttpResponse(mi_template.render())
def man3(request):
    mi_template = loader.get_template("manual/m3.html")
    return HttpResponse(mi_template.render())
def man4(request):
    mi_template = loader.get_template("manual/m4.html")
    return HttpResponse(mi_template.render())
def man5(request):
    mi_template = loader.get_template("manual/m5.html")
    return HttpResponse(mi_template.render())


@login_required(login_url='login')
def v_inicio_admin(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("inicio_admin.html")
    mi_contexto = {'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def v_inicio(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("inicio.html")
    servicios = Servicio.objects.all()
    mi_contexto = {'servicios':servicios,'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def Prestamo(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("auto_prestamo.html")
    computadores = Computador.objects.all()
    servicios = Servicio.objects.all()
    mi_contexto = {'computadores':computadores,'servicios':servicios,'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def SolicitarServicio(request,pk,template_name='agregar/solicitar_servicio.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Servicio, pk=pk)
    servicios = Servicio.objects.all()
    if request.method=='POST':
        solicitud = SolicitudServicio(per_cedula=usuario, carr_id=usuario.carr_id,serv_id=obj,comp_id=None,ss_estado=True)
        solicitud.save()
        return redirect("logout")
    return render(request,template_name,{'servicios':servicios,'serv':obj,'user':usuario})

@login_required(login_url='login')
def HistorialSolicitud(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("listar/historial.html")
    solicitudes = SolicitudServicio.objects.order_by('-ss_fecha')
    paginator2 = Paginator(solicitudes, 25)
    page2 = request.GET.get('page')
    try:
        contacts2 = paginator2.page(page2)
    except PageNotAnInteger:
        contacts2 = paginator2.page(1)
    except EmptyPage:
        contacts2 = paginator2.page(paginator2.num_pages)
    mi_contexto={'solicitudes':contacts2,'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def UsuarioUpdateADM(request,pk,template_name='editar/editUser.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    us=get_object_or_404(User,per_cedula=pk)
    form = UserFormADM(request.POST or None,instance=us)
    if form.is_valid():
        form.save()
        return redirect("personas_list")
    return render(request,template_name,{'form':form,'user':usuario})

def UsuaioCreate(request, template_name='agregar/agregar_usuario.html'):
    passw=GenPasswd(4).lower()
    form = UserForm(request.POST or None)
    if form.is_valid():
        cedula=request.POST.get("per_cedula")
        nombre=request.POST.get("per_nombre")
        apellido=request.POST.get("per_apellido")
        carrera=request.POST.get("carr_id")
        tipo=request.POST.get("tip_id")
        contra=request.POST.get("contra")

        carr = get_object_or_404(Carrera, carr_id=carrera)
        tip = get_object_or_404(Tipo_persona, tip_id=tipo)

        User.object.create_user(cedula,nombre,apellido,contra,contra,carr_id=carr,tip_id=tip)
        return redirect("login")
    return render(request,template_name,{'form':form,'clave':passw})

@login_required(login_url='login')
def UsuarioUpdate(request,template_name='editar/editar_usuario.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = UserForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect("inicio")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='/')
def PersonaDelete(request,pk):
    obj = get_object_or_404(User, pk=pk)
    obj.is_active=False
    obj.save()
    return redirect("personas_list")

@login_required(login_url='login')
def editar_contrasena(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.per_pass2=form.cleaned_data['password']
            request.user.save()
            return redirect('inicio')
    else:
        form = EditarContrasenaForm()
    return render(request, 'editar/editar_contrasena.html', {'form': form,'user':usuario})

# -------------------------------------------------------servicios--------------------------------------------------------------
@login_required(login_url='login')
def ServicioCreate(request, template_name='agregar/agregar_servicio.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = ServiciosForm(request.POST or None)
    servicios = Servicio.objects.all()
    if form.is_valid():
        form.save()
        return redirect("serv_list")
    return render(request,template_name,{'form':form,'servicios':servicios,'user':usuario})

@login_required(login_url='login')
def Servicios(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        serv = Servicio.objects.order_by("serv_id").filter(serv_nombre__contains=request.POST["busca"])
        return render_to_response('listar/servicios.html',{'servicios':serv,'user':usuario},context_instance=RequestContext(request))
    serv = Servicio.objects.order_by("serv_id")
    return render_to_response('listar/servicios.html',{'servicios':serv,'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='login')
def ServicioUpdate(request,pk,template_name='editar/editar_servicio.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Servicio, pk=pk)
    form = ServiciosForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("serv_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='/')
def ServicioDelete(request,pk):
    obj = get_object_or_404(Servicio, pk=pk)
    obj.serv_estado=False
    obj.save()
    return redirect("serv_list")

# -------------------------------------------------------computadoras--------------------------------------------------------------
@login_required(login_url='login')
def ComputadorCreate(request, template_name='agregar/agregar_computador.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = ComputadorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("comp_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='login')
def Computadoras(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        comp = Computador.objects.order_by("comp_numero").filter(comp_numero__contains=request.POST["busca"])
        return render_to_response('listar/computadoras.html',{'computadoras':comp,'user':usuario},context_instance=RequestContext(request))
    comp = Computador.objects.order_by("comp_numero")
    return render_to_response('listar/computadoras.html',{'computadoras':comp,'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='login')
def ComputadorUpdate(request,pk,template_name='editar/editar_computador.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Computador, pk=pk)
    form = ComputadorForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("comp_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='/')
def ComputadorDelete(request,pk):
    obj = get_object_or_404(Computador, pk=pk)
    obj.comp_estado=False
    obj.save()
    return redirect("comp_list")

@login_required(login_url='login')
def Agregar_observacion(request,pk,template_name='agregar/agregar_observacion.html'):
    comp = get_object_or_404(Computador, pk=pk)
    if request.method=='POST':
        ob = Observaciones(ob_observacion=request.POST.get("observacion"),comp_id=comp)
        ob.save()
        return redirect("comp_list")
    return render(request,template_name,{'computador':comp})

@login_required(login_url='login')
def Ver_observacion(request,pk,template_name='listar/observaciones.html'):
    comp = get_object_or_404(Computador, pk=pk)
    obs = Observaciones.objects.order_by("ob_fecha").filter(comp_id=comp).values()
    return render(request,template_name,{'computador':comp,'observaciones':obs})

# -------------------------------------------------------unidades--------------------------------------------------------------
@login_required(login_url='login')
def UACreate(request, template_name='agregar/agregar_unidad.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = U_A_Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("ua_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='login')
def UA(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        ua = Unidad_academica.objects.order_by("ua_id").filter(ua_nombre__contains=request.POST["busca"])
        return render_to_response('listar/unidades.html',{'unidades':ua,'user':usuario},context_instance=RequestContext(request))
    ua = Unidad_academica.objects.order_by("ua_id")
    return render_to_response('listar/unidades.html',{'unidades':ua,'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='login')
def UAUpdate(request,pk,template_name='editar/editar_unidad.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Unidad_academica, pk=pk)
    form = U_A_Form(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("ua_list")
    return render(request,template_name,{'form':form,'user':usuario})

# -------------------------------------------------------Carreras--------------------------------------------------------------
@login_required(login_url='login')
def CarreraCreate(request, template_name='agregar/agregar_carrera.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = CarreraForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("carreras_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='login')
def Carreras(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        carr = Carrera.objects.order_by("carr_id").filter(carr_nombre__contains=request.POST["busca"])
        return render_to_response('listar/carreras.html',{'carreras':carr,'user':usuario},context_instance=RequestContext(request))
    carr = Carrera.objects.order_by("carr_id")
    return render_to_response('listar/carreras.html',{'carreras':carr,'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='login')
def CarreraUpdate(request,pk,template_name='editar/editar_carrera.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Carrera, pk=pk)
    form = CarreraForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("carreras_list")
    return render(request,template_name,{'form':form,'user':usuario})

# -------------------------------------------------------tipos--------------------------------------------------------------
@login_required(login_url='login')
def TipoCreate(request, template_name='agregar/agregar_tipo.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = TipoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("tipos_list")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='login')
def Tipos(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        tips = Tipo_persona.objects.order_by("tip_id").filter(tip_nombre__contains=request.POST["busca"])
        return render_to_response('listar/tipos.html',{'tipos':tips,'user':usuario},context_instance=RequestContext(request))
    tips = Tipo_persona.objects.order_by("tip_id")
    return render_to_response('listar/tipos.html',{'tipos':tips,'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='/')
def TipoUpdate(request,pk,template_name='editar/editar_tipo.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj = get_object_or_404(Tipo_persona, pk=pk)
    form = TipoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("tipos_list")
    return render(request,template_name,{'form':form,'user':usuario})

# -------------------------------------------------------personas--------------------------------------------------------------
@login_required(login_url='login')
def Personas(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        usuarios = User.object.order_by("per_cedula").filter(per_cedula__contains=request.POST["busca"])
        paginator2 = Paginator(usuarios, 25)
        page2 = request.GET.get('page')
        try:
            contacts2 = paginator2.page(page2)
        except PageNotAnInteger:
            contacts2 = paginator2.page(1)
        except EmptyPage:
            contacts2 = paginator2.page(paginator2.num_pages)
        return render(request,'listar/personas.html',{'users':contacts2,'user':usuario})

    usuarios = User.object.order_by("per_cedula")
    paginator2 = Paginator(usuarios, 25)
    page2 = request.GET.get('page')
    try:
        contacts2 = paginator2.page(page2)
    except PageNotAnInteger:
        contacts2 = paginator2.page(1)
    except EmptyPage:
        contacts2 = paginator2.page(paginator2.num_pages)
    return render(request,'listar/personas.html',{'users':contacts2,'user':usuario})

#-----------------------------------------------------Importar Usuarios------------------------------------------------------
@login_required(login_url='/')
def Importar(request,pk,pk2):
    dataReader = csv.reader(open(pk), delimiter=';', quotechar='"')
    usuario=get_object_or_404(User,per_cedula=request.user)
    for row in dataReader:
        if usuario.per_cedula=="0"+str(row[0]).decode("latin1"):
            print("")
        else:
            if len(str(row[0]).decode("latin1"))<10:
                contra="0"+str(row[0]).decode("latin1")
                cedula="0"+str(row[0]).decode("latin1")
            else:
                contra=str(row[0]).decode("latin1")
                cedula=str(row[0]).decode("latin1")

            nombre=str(row[2]).decode("latin1")
            apellido=str(row[1]).decode("latin1")

            carrera=get_object_or_404(Carrera,carr_nombre=pk2)

            User.object.create_user(cedula,nombre,apellido,contra,contra,carr_id=carrera,tip_id=None)
    return redirect("personas_list")

@login_required(login_url='login')
def Archivos_I(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("archivos.html")
    importe = Importe.objects.all()
    mi_contexto = {'importe':importe,'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def ArchivoCreate(request, template_name='agregar/agregar_archivo.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    form = ImporteForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return redirect("importar")
    return render(request,template_name,{'form':form,'user':usuario})

@login_required(login_url='login')
def Eliminar_por_carrera(request,template_name='eliminar_c.html'):
    usuario=get_object_or_404(User,per_cedula=request.user)
    obj2=Carrera.objects.all()
    if request.method == 'POST':
        obj = User.object.all()
        obj3=get_object_or_404(Carrera,carr_id=request.POST['carr'])
        for i in obj:
            if i.carr_id == obj3:
                i.delete()
        return redirect("personas_list")
    return render(request,template_name,{'carreras':obj2,'user':usuario})

# --------------------------------------------------------reportes----------------------------------------------
@login_required(login_url='login')
def Reportes_solicitudes(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    mi_template = loader.get_template("repotes.html")
    mi_contexto = {'user':usuario}
    return HttpResponse(mi_template.render(mi_contexto))

@login_required(login_url='login')
def Reportes_solicitudes_est(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Solicitudes.pdf"
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=40,leftMargin=50,topMargin=60,bottomMargin=18,)
        usuarios = []
        styles = getSampleStyleSheet()
        us=get_object_or_404(User,per_cedula__contains=request.POST["resul"])
        header = Paragraph("Listado de Solicitudes de "+us.per_nombre+" "+us.per_apellido, styles['Heading1'])
        usuarios.append(header)
        contador=0
        obj1=SolicitudServicio.objects.order_by("per_cedula").filter(per_cedula_id=request.POST["resul"]).values()
        for b in obj1:
            contador+=1
        headings = ('Usuario', 'Carrera', 'Servicio', 'Fecha')
        allusuarios = [(p.per_cedula, p.carr_id, p.serv_id, p.ss_fecha.date()) for p in SolicitudServicio.objects.order_by("per_cedula").filter(per_cedula_id=request.POST["resul"])]
        t = Table([headings] + allusuarios)
        t.setStyle(TableStyle(
            [('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        usuarios.append(t)
        numero = Paragraph("Total de registros: "+str(contador), styles['Heading3'])
        usuarios.append(numero)
        doc.build(usuarios)
        response.write(buff.getvalue())
        buff.close()
        return response
    return render_to_response('rep_por_estudiante.html',{'user':usuario},context_instance=RequestContext(request))

@login_required(login_url='login')
def Reportes_solicitudes_carr(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    carreras=Carrera.objects.all()
    if request.method=='POST':
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Solicitudes.pdf"
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=40,leftMargin=50,topMargin=60,bottomMargin=18,)
        usuarios = []
        styles = getSampleStyleSheet()
        car=get_object_or_404(Carrera,carr_id=request.POST["resul"])
        header = Paragraph("Listado de Solicitudes de "+car.carr_nombre, styles['Heading1'])
        usuarios.append(header)
        headings = ('Usuario', 'Carrera', 'Servicio', 'Fecha')
        contador=0
        obj1=SolicitudServicio.objects.order_by("carr_id").filter(carr_id_id=request.POST["resul"]).values()
        for b in obj1:
            contador+=1

        allusuarios = [(p.per_cedula, p.carr_id, p.serv_id, p.ss_fecha.date())
                       for p in SolicitudServicio.objects.order_by("carr_id").filter(carr_id_id=request.POST["resul"])
                       ]
        t = Table([headings] + allusuarios)
        t.setStyle(TableStyle(
            [('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        usuarios.append(t)
        numero = Paragraph("Total de registros: "+str(contador), styles['Heading3'])
        usuarios.append(numero)
        doc.build(usuarios)
        response.write(buff.getvalue())
        buff.close()
        return response
    return render_to_response('rep_por_carrera.html',{'user':usuario,'carr':carreras},context_instance=RequestContext(request))

@login_required(login_url='login')
def Reportes_solicitudes_serv(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    serv=Servicio.objects.all()
    if request.method=='POST':
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Solicitudes.pdf"
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=40,leftMargin=50,topMargin=60,bottomMargin=18,)
        usuarios = []
        styles = getSampleStyleSheet()
        car=get_object_or_404(Servicio,serv_id=request.POST["resul"])
        header = Paragraph("Listado de "+car.serv_nombre, styles['Heading1'])
        usuarios.append(header)
        headings = ('Usuario', 'Carrera', 'Servicio', 'Fecha')
        contador=0
        obj1=SolicitudServicio.objects.order_by("serv_id").filter(serv_id_id=request.POST["resul"]).values()
        for b in obj1:
            contador+=1

        allusuarios = [(p.per_cedula, p.carr_id, p.serv_id, p.ss_fecha.date())
                       for p in SolicitudServicio.objects.order_by("serv_id").filter(serv_id_id=request.POST["resul"])
                       ]
        t = Table([headings] + allusuarios)
        t.setStyle(TableStyle(
            [('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        usuarios.append(t)
        numero = Paragraph("Total de registros: "+str(contador), styles['Heading3'])
        usuarios.append(numero)
        doc.build(usuarios)
        response.write(buff.getvalue())
        buff.close()
        return response
    return render_to_response('rep_por_servicio.html',{'user':usuario,'serv':serv},context_instance=RequestContext(request))

@login_required(login_url='login')
def Reportes_solicitudes_fech(request):
    usuario=get_object_or_404(User,per_cedula=request.user)
    if request.method=='POST':

        response = HttpResponse(content_type='application/pdf')
        pdf_name = "Solicitudes.pdf"
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=40,leftMargin=50,topMargin=60,bottomMargin=18,)
        usuarios = []
        styles = getSampleStyleSheet()
        header = Paragraph("Listado de Solicitudes del "+request.POST["resul"], styles['Heading1'])
        usuarios.append(header)
        obj=SolicitudServicio.objects.all()
        obj2=[]
        contador=0
        for a in obj:
            if str(a.ss_fecha.date()) == str(request.POST["resul"]):
                contador+=1
                obj2.append(a)

        headings = ('Usuario', 'Carrera', 'Servicio', 'Fecha')
        allusuarios = [(p.per_cedula, p.carr_id, p.serv_id, p.ss_fecha) for p in obj2]
        t = Table([headings] + allusuarios)
        t.setStyle(TableStyle(
            [('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        usuarios.append(t)
        numero = Paragraph("Total de registros: "+str(contador), styles['Heading3'])
        usuarios.append(numero)
        doc.build(usuarios)
        response.write(buff.getvalue())
        buff.close()
        return response
    return render_to_response('rep_por_fecha.html',{'user':usuario},context_instance=RequestContext(request))

def generar_pdf_Usuario(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "empleados.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=50,leftMargin=50,topMargin=60,bottomMargin=18,)
    usuarios = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Usuarios", styles['Heading2'])
    usuarios.append(header)
    headings = ('Cédula', 'Nombres', 'Apellidos', 'Carrera', 'Estado')
    allusuarios = [(p.per_cedula, p.per_nombre, p.per_apellido, p.carr_id, p.is_active) for p in User.object.all()]
    t = Table([headings] + allusuarios)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    usuarios.append(t)
    doc.build(usuarios)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_pdf_Computador(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Computadoras.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    usuarios = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Computadoras", styles['Heading1'])
    usuarios.append(header)
    headings = ('Mac', 'Numero', 'Marca', 'No. Serie','Sistema Operativo', 'Año', 'RAM', 'Procesador', 'Estado')
    allusuarios = [(p.comp_id, p.comp_numero, p.comp_marca, p.comp_serie, p.comp_so, p.comp_anio, p.comp_ram, p.comp_procesador, p.comp_estado) for p in Computador.objects.all()]
    t = Table([headings] + allusuarios)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    usuarios.append(t)
    doc.build(usuarios)
    response.write(buff.getvalue())
    buff.close()
    return response

# -----------------------------------------------------Reportes de solicitudes -------------------------------------------------

def Pdf_solicutud_general(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Solicitudes.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=40,leftMargin=40,topMargin=60,bottomMargin=18,)
    usuarios = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Solicitudes", styles['Heading1'])
    usuarios.append(header)
    contador=0
    obj1=SolicitudServicio.objects.all()
    for b in obj1:
        contador+=1
    headings = ('Usuario', 'Carrera', 'Servicio', 'Fecha')
    allusuarios = [(p.per_cedula, p.carr_id, p.serv_id, p.ss_fecha.date()) for p in SolicitudServicio.objects.all()]
    t = Table([headings] + allusuarios)
    t.setStyle(TableStyle(
        [('GRID', (0, 0), (8, -1), 1, colors.dodgerblue),('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    usuarios.append(t)
    numero = Paragraph("Total de registros: "+str(contador), styles['Heading3'])
    usuarios.append(numero)
    doc.build(usuarios)
    response.write(buff.getvalue())
    buff.close()
    return response
