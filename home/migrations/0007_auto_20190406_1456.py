# Generated by Django 2.1.7 on 2019-04-06 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_sex_userprofile_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Sex'),
        ),
    ]