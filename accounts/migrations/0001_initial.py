# Generated by Django 3.0.3 on 2020-05-02 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(max_length=30, null=True, verbose_name='Customer Name')),
                ('cust_location', models.CharField(max_length=50, null=True, verbose_name='Customer Location')),
                ('cust_phone', models.CharField(max_length=20, null=True, verbose_name='Customer Phone Number')),
                ('cust_date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
