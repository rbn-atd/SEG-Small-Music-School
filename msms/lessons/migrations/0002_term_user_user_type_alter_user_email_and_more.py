# Generated by Django 4.1.3 on 2022-12-05 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_number', models.PositiveIntegerField(unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Dev'), (1, 'Student'), (2, 'Admin'), (3, 'Director')], default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', multiselectfield.db.fields.MultiSelectField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=57)),
                ('number_Of_Lessons', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='1', max_length=1)),
                ('length', models.CharField(choices=[('30 mins', '30 mins'), ('60 mins', '60 mins'), ('90 mins', '90 mins')], default='30 mins', max_length=7)),
                ('interval', models.CharField(choices=[('every week', 'every week'), ('every 2 weeks', 'every 2 weeks'), ('every 3 weeks', 'every 3 weeks'), ('every 4 weeks', 'every 4 weeks')], default='every week', max_length=13)),
                ('body', models.TextField(blank=True, max_length=200)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepting_admin', models.CharField(max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid', models.BooleanField()),
                ('invoice_number', models.CharField(max_length=50, unique=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.request')),
            ],
        ),
    ]
