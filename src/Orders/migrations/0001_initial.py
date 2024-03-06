# Generated by Django 5.0.2 on 2024-03-06 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BasicInfo', '0001_initial'),
        ('Patients', '0001_initial'),
        ('Personnel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(max_length=50, verbose_name='نام خانوادگی')),
                ('gender', models.CharField(choices=[('M', 'مرد'), ('F', 'زن')], max_length=1, verbose_name='جنسیت')),
                ('national_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
            ],
            options={
                'verbose_name': 'کارفرما',
                'verbose_name_plural': 'کارفرما ها',
            },
        ),
        migrations.CreateModel(
            name='ClientAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_text', models.CharField(max_length=250, verbose_name='آدرس')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.client')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
        migrations.CreateModel(
            name='CareContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('care_for', models.CharField(choices=[('E', 'سالمند'), ('P', 'مددجو'), ('K', 'کودک')], max_length=1, verbose_name='مراقبت از')),
                ('shift', models.CharField(choices=[('D', 'روزانه'), ('N', 'شبانه'), ('B', 'شبانه روزی'), ('O', 'سایر')], max_length=1, verbose_name='شیفت')),
                ('shift_start', models.PositiveSmallIntegerField(default=8, verbose_name='ساعت شروع شیفت')),
                ('shift_end', models.PositiveSmallIntegerField(default=18, verbose_name='ساعت پایان شیفت')),
                ('relationship_with_patient', models.CharField(choices=[('S', 'خودشان'), ('C', 'فرزند'), ('P', 'همسر'), ('O', 'سایر')], max_length=1, verbose_name='نسبت با بیمار')),
                ('relationship_with_patient_note', models.CharField(blank=True, help_text='در صورتی که رابطه با فرد متقاضی خدمت سایر بود، نسبت دقیق آنها در این فیلد نوشته شود.', max_length=150, null=True, verbose_name='نسبت با بیمار')),
                ('start', models.DateTimeField(verbose_name='شروع قرارداد')),
                ('end', models.DateTimeField(verbose_name='پایان قرارداد')),
                ('include_holidays', models.BooleanField(default=True, help_text='در تعطیلات رسمی از طرف هیات دولت پرسنل تعطیل نمی باشند', verbose_name='شامل تعطیلات می شود')),
                ('personnel_monthly_salary', models.IntegerField(default=0, verbose_name='حقوق ماهانه پرسنل')),
                ('personnel_salary_payment_time', models.CharField(choices=[('S', 'ابتدای ماه'), ('E', 'انتهای ماه'), ('O', 'سایر')], max_length=1, verbose_name='تسویه با پرسنل')),
                ('healthcare_franchise_amount', models.IntegerField(default=0, help_text='مبلغ فرانشیز مرکز به تومان', verbose_name='فرانشیز مرکز')),
                ('client_payment_status', models.CharField(choices=[('PAPD', 'پرداخت جزیی'), ('COPD', 'پرداخت کامل'), ('NOPD', 'پرداخت نشده')], default='NOPD', max_length=4, verbose_name='وضعیت تسفیه حساب کارفرما')),
                ('personnel_payment_status', models.CharField(choices=[('PAPD', 'پرداخت جزیی'), ('COPD', 'پرداخت کامل'), ('NOPD', 'پرداخت نشده')], default='NOPD', max_length=4, verbose_name='وضعیت تسفیه حساب پرسنل')),
                ('patients', models.ManyToManyField(to='Patients.patient', verbose_name='مددجو/ سالمند/ کودک')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Personnel.personnel', verbose_name='پرسنل')),
                ('referral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogcallreferral', verbose_name='نوع معرفی')),
                ('referral_other_healthcare', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogmedicalcenter', verbose_name='مرکز همکار معرف')),
                ('referral_personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personnel_%(class)s_referral', to='Personnel.personnel', verbose_name='همکار معرف')),
                ('shift_days', models.ManyToManyField(to='BasicInfo.weekday', verbose_name='روز های شیفت')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.client', verbose_name='کارفرما')),
                ('referral_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_%(class)s_referral', to='Orders.client', verbose_name='کارفرما معرف')),
                ('service_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.clientaddress', verbose_name='محل خدمت')),
            ],
            options={
                'verbose_name': 'قرار داد مراقبت',
                'verbose_name_plural': 'قرارداد های مراقبت',
            },
        ),
        migrations.CreateModel(
            name='ClientPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_type', models.CharField(choices=[('N', 'شماره تماس عادی'), ('E', 'شماره تماس اضطراری')], default='N', max_length=1, verbose_name='نوع شماره')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تلفن همراه')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.client', verbose_name='کارفرما')),
            ],
            options={
                'verbose_name': 'شماره تماس',
                'verbose_name_plural': 'شماره های تماس',
            },
        ),
        migrations.CreateModel(
            name='ContractComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250, verbose_name='کامنت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.carecontract', verbose_name='قراردار')),
            ],
            options={
                'verbose_name': ' کامنت قرارداد',
                'verbose_name_plural': 'کامنت های قرارداد',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested', models.DateTimeField(auto_now_add=True, verbose_name='زمان درخواست')),
                ('accepted', models.DateTimeField(blank=True, null=True, verbose_name='زمان قبول درخواست توسط پرسنل')),
                ('done', models.DateTimeField(blank=True, null=True, verbose_name='زمان اتمام')),
                ('order_status', models.CharField(choices=[('DON', 'انجام شده'), ('ASG', 'محول شده'), ('WLS', 'لیست انتظار'), ('CPT', 'لغو شده')], default='WLS', max_length=3, verbose_name='وضعیت درخواست')),
                ('client_payment_status', models.CharField(choices=[('PAPD', 'پرداخت جزیی'), ('COPD', 'پرداخت کامل'), ('NOPD', 'پرداخت نشده')], default='NOPD', max_length=4, verbose_name='وضعیت پرداخت کارفرما')),
                ('personnel_payment_status', models.CharField(choices=[('PAPD', 'پرداخت جزیی'), ('COPD', 'پرداخت کامل'), ('NOPD', 'پرداخت نشده')], default='NOPD', max_length=4, verbose_name='وضعیت پرداخت پرسنل')),
                ('discount', models.IntegerField(default=0, help_text='به تومان', verbose_name='تخفیف')),
                ('assigned_personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='Personnel.personnel', verbose_name='پرسنل')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Orders.client', verbose_name='کارفرما')),
                ('patient_tag_specifications', models.ManyToManyField(blank=True, to='BasicInfo.catalogtagspecification', verbose_name='خصوصیات درخواست دهنده')),
                ('referral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogcallreferral', verbose_name='معرف')),
                ('referral_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_orders_referral', to='Orders.client', verbose_name='کارفرما معرف')),
                ('referral_other_healthcare', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogmedicalcenter', verbose_name='مرکز همکار معرف')),
                ('referral_personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personnel_orders_referral', to='Personnel.personnel', verbose_name='همکار معرف')),
                ('service_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.clientaddress', verbose_name='محل خدمت')),
            ],
            options={
                'verbose_name': 'خدمت موردی',
                'verbose_name_plural': 'خدمات موردی',
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250, verbose_name='کامنت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Orders.order', verbose_name='خدمت موردی')),
            ],
            options={
                'verbose_name': ' کامنت سفارش',
                'verbose_name_plural': 'کامنت های سفارش',
            },
        ),
        migrations.CreateModel(
            name='OrderService',
            fields=[
                ('junction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='BasicInfo.junction')),
                ('cost', models.IntegerField(default=0, help_text='به تومان', verbose_name='هزینه')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.order', verbose_name='خدمت موردی')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogservice', verbose_name='سرویس')),
            ],
            options={
                'verbose_name': 'سرویس خدمت موردی',
                'verbose_name_plural': 'سرویس های خدمت موردی',
            },
            bases=('BasicInfo.junction',),
        ),
    ]
