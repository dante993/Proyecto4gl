# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
from django.db import connection

import cx_Oracle

class Data_bd:
    def __enter__(self):
        #self.__db = cx_Oracle.Connection( "{USER}usercine/usercine@192.168.239.131:1521/orcl.example.com")
        db_conf = getattr(settings, "DATABASES", None)['default']
        self.__db = cx_Oracle.Connection( "usuaroi/contrase@servidor:puerto/nombreorcl".format(**db_conf))
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.__cursor.close()
        self.__db.close()

    def execute_proc_as_list(self, proc_name, params):
        # params doesnt need that have CURSOR type
        cursor_var = self.__cursor.var(cx_Oracle.CURSOR)
        params.append(cursor_var)
        l_query, listado = self.__cursor.callproc(proc_name, params)
        # there are no OUT parameters in Python, regular return here
        return list(listado)

    def execute_proc(self, proc_name, params):
        # Execute procedures without return nothing (insert, update, delete)
        cx_query = self.__cursor.callproc(proc_name, params)
        return cx_query

class Servicio(models.Model):
    serv_id=models.AutoField(primary_key=True)
    serv_nombre = models.CharField(max_length = 60)
    serv_descripcion=models.TextField()
    serv_estado = models.BooleanField()
    def __unicode__(self):
        return self.serv_nombre
    def serv_create(self,serv_nombre,serv_descripcion,serv_estado):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("CREAR_SERVICIO", (serv_nombre,serv_descripcion,serv_estado,msgrt))
        cursor.close()
        return ret
    def serv_list(self):
        vista_servicio = []
        cur = connection.cursor()
        cursor = cur.var(cx_Oracle.CURSOR).var
        query = cur.callproc('LISTAR_SERVICIO', ("", cursor))
        for row in query[1].fetchall():
            vista_servicio.append({'serv_id': row[0],
                                'serv_nombre': row[1],
                                'serv_descripcion': row[2],
                                'serv_estado': row[3]})
        print(vista_servicio)
        cur.close()
        return vista_servicio
    def serv_update(self,serv_id,serv_nombre,serv_descripcion,serv_estado):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("ACTUALIZAR_SERVICIO", (serv_id,serv_nombre,serv_descripcion,serv_estado,msgrt))
        cursor.close()
        return ret
    def serv_delete(self,serv_id):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("ELIMINAR_SERVICIO", (serv_id,msgrt))
        cursor.close()
        return ret

class Sensor(models.Model):
    sens_id=models.AutoField(primary_key=True)
    sens_fecha = models.DateField(auto_now=True)
    sens_estado = models.BooleanField()

class Computador(models.Model):
    comp_id=models.CharField(primary_key=True,max_length = 17,unique=True)
    comp_numero = models.CharField(max_length = 10)
    comp_marca=models.CharField(max_length = 50)
    comp_serie=models.CharField(max_length = 50)
    comp_so=models.CharField(max_length = 50)
    comp_anio=models.CharField(max_length = 50,verbose_name='año')
    comp_ram=models.CharField(max_length = 50)
    comp_disco_d=models.CharField(max_length = 50)
    comp_procesador=models.CharField(max_length = 50)
    comp_uso=models.BooleanField(default=False)
    comp_estado = models.BooleanField()
    def comp_create(self,comp_id, comp_numero,comp_marca,comp_serie,comp_so,comp_anio,comp_ram,comp_disco_d,comp_procesador,comp_uso,comp_estado):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("CREAR_COMPUTADOR", (comp_id,comp_numero,comp_marca,comp_serie,comp_so,comp_anio,comp_ram,comp_disco_d,comp_procesador,comp_uso,comp_estado,msgrt))
        cursor.close()
        return ret
    def comp_list(self):
        vista_computador = []
        cur = connection.cursor()
        cursor = cur.var(cx_Oracle.CURSOR).var
        query = cur.callproc('LISTAR_COMPUTADOR', ("", cursor))
        for row in query[1].fetchall():
            vista_computador.append({'comp_id': row[0],
                                'comp_numero': row[1],
                                'comp_marca': row[2],
                                'comp_serie': row[3],
                                'comp_so': row[4],
                                'comp_anio': row[5],
                                'comp_ram': row[6],
                                'comp_disco_d': row[7],
                                'comp_procesador': row[8],
                                'comp_uso': row[9],
                                'comp_estado': row[10]})
        print(vista_computador)
        cur.close()
        return vista_computador
    def comp_update(self,comp_id, comp_numero,comp_marca,comp_serie,comp_so,comp_anio,comp_ram,comp_disco_d,comp_procesador,comp_uso,comp_estado):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("ACTUALIZAR_COMPUTADOR", (comp_id,comp_numero,comp_marca,comp_serie,comp_so,comp_anio,comp_ram,comp_disco_d,comp_procesador,comp_uso,comp_estado,msgrt))
        cursor.close()
        return ret
    def comp_delete(self,comp_id):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("ELIMINAR_COMPUTADOR", (comp_id,msgrt))
        cursor.close()
        return ret

class Observaciones(models.Model):
    ob_id=models.AutoField(primary_key=True)
    ob_observacion=models.TextField()
    ob_fecha=models.CharField(max_length=50)
    comp_id=models.ForeignKey(Computador)
    def ob_create(self, ob_observacion,ob_fecha,comp_id):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("CREAR_OBSERVACIONES", (ob_observacion,ob_fecha,comp_id,msgrt))
        cursor.close()
        return ret
    def ob_list(self):
        vista_observacion = []
        cur = connection.cursor()
        cursor = cur.var(cx_Oracle.CURSOR).var
        query = cur.callproc('LISTAR_OBSERVACIONES', ("", cursor))
        for row in query[1].fetchall():
            vista_observacion.append({'ob_observacion': row[1],
                                'ob_fecha': row[2],
                                'comp_id': row[3]})
        print(vista_observacion)
        cur.close()
        return vista_observacion


class Unidad_academica(models.Model):
    ua_id=models.AutoField(primary_key=True)
    ua_nombre = models.CharField(max_length = 60)
    ua_descripcion=models.TextField()
    dep_codigo = models.IntegerField()
    def __unicode__(self):
        return self.ua_nombre


class Carrera(models.Model):
    carr_id=models.AutoField(primary_key=True)
    carr_nombre = models.CharField(max_length = 60)
    carr_descripcion=models.TextField()
    dep_codigo = models.IntegerField()
    ua_id=models.ForeignKey(Unidad_academica,verbose_name="Unidades académicas")
    def __unicode__(self):
        return self.carr_nombre

class Importe(models.Model):
    imp_archvio=models.FileField(upload_to="importes")
    imp_carrera=models.ForeignKey(Carrera)

class Tipo_persona(models.Model):
    tip_id=models.AutoField(primary_key=True)
    tip_nombre=models.CharField(max_length=50)
    def __unicode__(self):
        return self.tip_nombre
    def tip_create(self, tip_nombre):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("CREAR_TIPO_PERSONA", (tip_nombre,msgrt))
        cursor.close()
        return ret
    def tip_list(self):
        vista_observacion = []
        cur = connection.cursor()
        cursor = cur.var(cx_Oracle.CURSOR).var
        query = cur.callproc('LISTAR_TIPO_PERSONA', ("", cursor))
        for row in query[1].fetchall():
            vista_observacion.append({'tip_id': row[0],
                                'tip_nombre': row[1]})
        print(vista_observacion)
        cur.close()
        return vista_observacion
    def tip_update(self,tip_id, tip_nombre):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("ACTUALIZAR_TIPO_PERSONA", (tip_id,tip_nombre,msgrt))
        cursor.close()
        return ret



def validar_cedula(value):
        ced_cliente=value
        msg = "La Cédula introducida no es valida"
        if ced_cliente.isdigit():
            cant_num_cedula=len(ced_cliente.split()[0])
            msg = "La Cédula introducida no es valida"
            if cant_num_cedula == 10 :
                valores = [ int(ced_cliente[x]) * (2 - x % 2) for x in range(9) ]
                suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
                veri = 10 - (suma - (10 * (suma / 10)))
                if int(ced_cliente[9]) == int(str(veri)[-1:]):
                    return ced_cliente
                else:
                    raise forms.ValidationError(msg)
            else:raise forms.ValidationError(msg)
        else:raise forms.ValidationError("Esto no es un número de cédula")


class UserManager(BaseUserManager,models.Manager):
    def _create_user(self,per_cedula,per_nombre,per_apellido,per_pass2 ,password,is_staff,
                    is_superuser,**extra_fields):
        user = self.model(per_cedula=per_cedula,per_nombre=per_nombre,per_apellido=per_apellido,per_pass2=per_pass2,is_staff=is_staff,
                            is_active=True,is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,per_cedula,per_nombre,per_apellido,per_pass2,password,**extra_fields):
        return self._create_user(per_cedula,per_nombre,per_apellido,per_pass2,password,False,False,**extra_fields)

    def create_superuser(self,per_cedula,per_nombre,per_apellido,per_pass2,password,**extra_fields):
        return self._create_user(per_cedula,per_nombre,per_apellido,per_pass2,password,True,True,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    per_cedula = models.CharField(primary_key=True,max_length = 10,validators=[validar_cedula],verbose_name="Cédula",unique=True)
    per_nombre = models.CharField(max_length = 60)
    per_apellido = models.CharField(max_length = 60)
    per_pass2=models.CharField(max_length = 10)

    carr_id = models.ForeignKey(Carrera,null=True,verbose_name="Carrera")
    tip_id = models.ForeignKey(Tipo_persona,null=True,verbose_name="Categoría")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    object=UserManager()
    USERNAME_FIELD = 'per_cedula'
    REQUIRED_FIELDS = ['per_nombre','per_apellido','per_pass2']

class SolicitudServicio(models.Model):
    per_cedula = models.ForeignKey(User)
    carr_id = models.ForeignKey(Carrera,blank=True,null=True)
    serv_id = models.ForeignKey(Servicio)
    comp_id=models.ForeignKey(Computador,blank=True,null=True)
    ss_fecha=models.DateTimeField(auto_now_add=True)
    ss_estado = models.BooleanField(default=True)
    def sserv_create(self,per_cedula,carr_id,serv_id,comp_id,ss_fecha,ss_estado):
        msgrt=''
        cursor = connection.cursor()
        ret = cursor.callproc("CREAR_SOLICITUDSERVICIO", (per_cedula,carr_id,serv_id,comp_id,ss_fecha,ss_estado,msgrt))
        cursor.close()
        return ret
    def sserv_list(self):
        vista_servicio = []
        cur = connection.cursor()
        cursor = cur.var(cx_Oracle.CURSOR).var
        query = cur.callproc('LISTAR_SOLICITUDSERVICIO', ("", cursor))
        for row in query[1].fetchall():
            vista_servicio.append({'serv_id': row[0],
                                'serv_nombre': row[1],
                                'serv_descripcion': row[2],
                                'serv_estado': row[3]})
        print(vista_servicio)
        cur.close()
        return vista_servicio
