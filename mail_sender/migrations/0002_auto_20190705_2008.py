# Generated by Django 2.1.2 on 2019-07-05 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail_sender', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examplefroalaform',
            name='poster',
        ),
        migrations.DeleteModel(
            name='ExampleFroalaForm',
        ),
    ]
