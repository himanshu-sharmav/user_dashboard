# Generated by Django 3.2.23 on 2024-05-06 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_signup', '0003_blogcategory_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='name',
            field=models.CharField(choices=[('Mental Health', 'Mental Health'), ('Heart Disease', 'Heart Disease'), ('Covid19', 'Covid19'), ('Immunization', 'Immunization')], max_length=100),
        ),
    ]
