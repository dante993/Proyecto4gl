# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import LibSoft.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('carr_id', models.AutoField(serialize=False, primary_key=True)),
                ('carr_nombre', models.CharField(max_length=60)),
                ('carr_descripcion', models.TextField()),
                ('dep_codigo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Computador',
            fields=[
                ('comp_id', models.CharField(max_length=17, unique=True, serialize=False, primary_key=True)),
                ('comp_numero', models.CharField(max_length=10)),
                ('comp_marca', models.CharField(max_length=50)),
                ('comp_serie', models.CharField(max_length=50)),
                ('comp_so', models.CharField(max_length=50)),
                ('comp_anio', models.CharField(max_length=50, verbose_name=b'a\xc3\xb1o')),
                ('comp_ram', models.CharField(max_length=50)),
                ('comp_disco_d', models.CharField(max_length=50)),
                ('comp_procesador', models.CharField(max_length=50)),
                ('comp_uso', models.BooleanField(default=False)),
                ('comp_estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Importe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imp_archvio', models.FileField(upload_to=b'importes')),
                ('imp_carrera', models.ForeignKey(to='LibSoft.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Observaciones',
            fields=[
                ('ob_id', models.AutoField(serialize=False, primary_key=True)),
                ('ob_observacion', models.TextField()),
                ('ob_fecha', models.DateTimeField(auto_now_add=True)),
                ('comp_id', models.ForeignKey(to='LibSoft.Computador')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sens_id', models.AutoField(serialize=False, primary_key=True)),
                ('sens_fecha', models.DateField(auto_now=True)),
                ('sens_estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('serv_id', models.AutoField(serialize=False, primary_key=True)),
                ('serv_nombre', models.CharField(max_length=60)),
                ('serv_descripcion', models.TextField()),
                ('serv_estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudServicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ss_fecha', models.DateTimeField(auto_now_add=True)),
                ('ss_estado', models.BooleanField(default=True)),
                ('carr_id', models.ForeignKey(blank=True, to='LibSoft.Carrera', null=True)),
                ('comp_id', models.ForeignKey(blank=True, to='LibSoft.Computador', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_persona',
            fields=[
                ('tip_id', models.AutoField(serialize=False, primary_key=True)),
                ('tip_nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unidad_academica',
            fields=[
                ('ua_id', models.AutoField(serialize=False, primary_key=True)),
                ('ua_nombre', models.CharField(max_length=60)),
                ('ua_descripcion', models.TextField()),
                ('dep_codigo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('per_cedula', models.CharField(primary_key=True, serialize=False, max_length=10, validators=[LibSoft.models.validar_cedula], unique=True, verbose_name=b'C\xc3\xa9dula')),
                ('per_nombre', models.CharField(max_length=60)),
                ('per_apellido', models.CharField(max_length=60)),
                ('per_pass2', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('carr_id', models.ForeignKey(verbose_name=b'Carrera', to='LibSoft.Carrera', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('tip_id', models.ForeignKey(verbose_name=b'Categor\xc3\xada', to='LibSoft.Tipo_persona', null=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='solicitudservicio',
            name='per_cedula',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solicitudservicio',
            name='serv_id',
            field=models.ForeignKey(to='LibSoft.Servicio'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='ua_id',
            field=models.ForeignKey(verbose_name=b'Unidades acad\xc3\xa9micas', to='LibSoft.Unidad_academica'),
        ),
    ]
