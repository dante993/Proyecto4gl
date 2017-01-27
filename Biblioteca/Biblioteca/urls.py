# -*- encoding: utf-8 -*-
"""Biblioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from LibSoft.views import *

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', v_home, name='home'),

    url(r'^manual1/$', man1, name='ma1'),
    url(r'^manual2/$', man2, name='ma2'),
    url(r'^manual3/$', man3, name='ma3'),
    url(r'^manual4/$', man4, name='ma4'),
    url(r'^manual5/$', man5, name='ma5'),

    url(r'^inicio/$', v_inicio, name='inicio'),
    url(r'^admin/$', v_inicio_admin, name='inicio_admin'),

    url(r'^login/$','django.contrib.auth.views.login',{'template_name': 'login.html'},name='login'),
    url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),

    url(r'^prestamo/$', Prestamo, name='prestamo'),

    # -------------------------------------------------------usuarios--------------------------------------------------------------
    url(r'^registro/$', UsuaioCreate, name='user_create'),
    url(r'^editar_perfil/$', UsuarioUpdate, name='editar_usuario'),
    url(r'^admin/usuarios/editar_usuario/(?P<pk>.*)/$', UsuarioUpdateADM, name='editar_usuario_adm'),
    url(r'^cambio_clave/$', editar_contrasena, name='clave_edit'),
    url(r'^admin/usuarios/borrar/(?P<pk>.*)/$', PersonaDelete, name='borrar_per'),
    url(r'^admin/usuarios/$', Personas, name='personas_list'),
    url(r'^admin/usuarios/eliminar/$', Eliminar_por_carrera, name='eliminar_c'),

    # -------------------------------------------------------servicios--------------------------------------------------------------
    url(r'^admin/servicios/editar/(?P<pk>.*)/$', ServicioUpdate, name='editar_servicio'),
    url(r'^admin/servicios/borrar/(?P<pk>.*)/$', ServicioDelete, name='borrar_serv'),
    url(r'^admin/servicios/agregar_servicio/$', ServicioCreate, name='serv_create'),
    url(r'^admin/servicios/$', Servicios, name='serv_list'),

    # -------------------------------------------------------computadoras--------------------------------------------------------------
    url(r'^admin/computadoras/editar/(?P<pk>.*)/$', ComputadorUpdate, name='editar_computador'),
    url(r'^admin/computadoras/agregar_observacion/(?P<pk>.*)/$', Agregar_observacion, name='observacion_pc'),
    url(r'^admin/computadoras/agregar_computador/$', ComputadorCreate, name='comp_create'),
    url(r'^admin/computadoras/observaciones/(?P<pk>.*)/$', Ver_observacion, name='obs_list'),
    url(r'^admin/computadoras/borrar/(?P<pk>.*)/$', ComputadorDelete, name='borrar_comp'),
    url(r'^admin/computadoras/$', Computadoras, name='comp_list'),

    # -------------------------------------------------------unidades--------------------------------------------------------------
    url(r'^admin/unidades/editar/(?P<pk>.*)/$', UAUpdate, name='editar_unidad'),
    url(r'^admin/unidades/agregar_unidad/$', UACreate, name='ua_create'),
    url(r'^admin/unidades/$', UA, name='ua_list'),

    # -------------------------------------------------------carreras--------------------------------------------------------------
    url(r'^admin/carreras/editar/(?P<pk>.*)/$', CarreraUpdate, name='editar_carrera'),
    url(r'^admin/carreras/agregar_carrera/$', CarreraCreate, name='carr_create'),
    url(r'^admin/carreras/$', Carreras, name='carreras_list'),

    # -------------------------------------------------------tipos--------------------------------------------------------------
    url(r'^admin/tipos/editar/(?P<pk>.*)/$', TipoUpdate, name='editar_tipo'),
    url(r'^admin/tipos/agregar_tipo/$', TipoCreate, name='tip_create'),
    url(r'^admin/tipos/$', Tipos, name='tipos_list'),
    url(r'^admin/importar/$', Archivos_I, name='importar'),
    url(r'^admin/archivo/$', ArchivoCreate, name='archivo'),
    url(r'^admin/archivo/(?P<pk>.*)/carrera/(?P<pk2>.*)/$', Importar, name='imp'),

    # -------------------------------------------------------Reportes--------------------------------------------------------------

    url(r'^admin/reportes_por_estudiante/$', Reportes_solicitudes, name='rep_soli'),

    url(r'^admin/reportes_de_solicitudes_por_estudiantes/$', Reportes_solicitudes_est, name='rep_soli_est'),
    url(r'^admin/reportes_de_solicitudes_por_carrera/$', Reportes_solicitudes_carr, name='rep_soli_carr'),
    url(r'^admin/reportes_de_solicitudes_por_fecha/$', Reportes_solicitudes_fech, name='rep_soli_fech'),
    url(r'^admin/reportes_de_solicitudes_por_servicio/$', Reportes_solicitudes_serv, name='rep_soli_serv'),


    url(r'^admin/reporte_personas/$', generar_pdf_Usuario, name='pdf'),
    url(r'^admin/reporte_computadoras/$', generar_pdf_Computador, name='pdf_comp'),

    url(r'^admin/reportes_de_solicitudes/pdf/$', Pdf_solicutud_general, name='rep_soli_gen'),


    url(r'^admin/historial_de_solicitudes/$', HistorialSolicitud, name='hits_serv'),
    url(r'^solicitar_servicio/(?P<pk>.*)/$', SolicitarServicio, name='solicitar_servicio'),
    ]
