# Generated by Django 5.0.2 on 2024-03-06 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Orders', '0001_initial'),
        ('Personnel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان پرداخت')),
                ('paid_at', models.CharField(max_length=10)),
                ('paid_amount', models.PositiveBigIntegerField(verbose_name='مبلغ پرداختی')),
                ('to_card_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='شماره کارت مقصد')),
                ('payment_desc', models.CharField(blank=True, max_length=250, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.carecontract', verbose_name='قرارداد مربوطه')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.client', verbose_name='از طرف')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.order', verbose_name='خدمت موردی مربوطه')),
            ],
            options={
                'verbose_name': 'پرداخت کارفرما',
                'verbose_name_plural': 'پرداختی های کارفرما',
            },
        ),
        migrations.CreateModel(
            name='OutgoingPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان پرداخت')),
                ('paid_at', models.CharField(max_length=10)),
                ('paid_amount', models.PositiveBigIntegerField(verbose_name='مبلغ پرداختی')),
                ('to_card_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='شماره کارت مقصد')),
                ('payment_desc', models.CharField(blank=True, max_length=250, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.carecontract', verbose_name='قرارداد مربوطه')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.order', verbose_name='خدمت موردی مربوطه')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Personnel.personnel', verbose_name='به شخص')),
            ],
            options={
                'verbose_name': 'پرداخت پرسنل',
                'verbose_name_plural': 'پرداختی های پرسنل',
            },
        ),
    ]
