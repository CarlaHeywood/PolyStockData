# Generated by Django 4.1.5 on 2023-01-21 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=8)),
                ('closep', models.CharField(max_length=10)),
                ('previous_date', models.CharField(max_length=10)),
                ('cash_amount', models.CharField(max_length=10)),
                ('divfrequency', models.CharField(max_length=2)),
                ('pay_date', models.CharField(max_length=10)),
                ('declaration_date', models.CharField(max_length=10)),
                ('ex_dividend_date', models.CharField(max_length=10)),
                ('stock_name', models.CharField(max_length=250)),
                ('stock_type', models.CharField(max_length=250)),
                ('weburl', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('brandicon', models.CharField(max_length=250)),
                ('brandlogo', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=16)),
            ],
        ),
    ]