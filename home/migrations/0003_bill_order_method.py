# Generated by Django 2.1.7 on 2019-03-23 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190322_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='order_method',
            field=models.BooleanField(default=False),
        ),
    ]