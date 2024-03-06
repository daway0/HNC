# Generated by Django 5.0.2 on 2024-03-06 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('category', models.CharField(choices=[('DIS', 'منطقه'), ('NGB', 'محله'), ('ARE', 'محدوده')], max_length=3, verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محدوده مکانی',
                'verbose_name_plural': 'محدوده های مکانی',
            },
        ),
        migrations.CreateModel(
            name='CatalogCallReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': 'علت تماس',
                'verbose_name_plural': 'علت های تماس',
            },
        ),
        migrations.CreateModel(
            name='CatalogCallReferral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': 'نوع معرف',
                'verbose_name_plural': 'انواع معرف',
            },
        ),
        migrations.CreateModel(
            name='CatalogMedicalCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره همراه')),
            ],
            options={
                'verbose_name': 'مرکز همکار',
                'verbose_name_plural': 'مراکز همکار',
            },
        ),
        migrations.CreateModel(
            name='CatalogPersonnelRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': 'نقش پرسنل',
                'verbose_name_plural': 'نقش های پرسنل',
            },
        ),
        migrations.CreateModel(
            name='CatalogTagSpecificationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': ' دسته بندی ویژگی (تگ)',
                'verbose_name_plural': 'دسته بندی های ویژگی های تگ',
            },
        ),
        migrations.CreateModel(
            name='CatalogValuedSpecificationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': 'دسته بندی ویژگی مقداری',
                'verbose_name_plural': 'دسته بندی  های ویژگی های مقداری',
            },
        ),
        migrations.CreateModel(
            name='Junction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
            ],
            options={
                'verbose_name': 'روز هفته',
                'verbose_name_plural': 'روز های هفته',
            },
        ),
        migrations.CreateModel(
            name='CatalogService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('category_tree', models.CharField(blank=True, max_length=250, null=True)),
                ('healthcare_franchise', models.PositiveSmallIntegerField(default=100, verbose_name='سهم مرکز')),
                ('base_price', models.IntegerField(default=0, verbose_name='قیمت پایه سرویس')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='BasicInfo.catalogservice')),
            ],
            options={
                'verbose_name': 'سرویس',
                'verbose_name_plural': 'سرویس ها',
            },
        ),
        migrations.CreateModel(
            name='CatalogServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BasicInfo.catalogservicecategory', verbose_name='دسته بندی')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CatalogTagSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('for_who', models.CharField(choices=[('PRS', 'پرسنل'), ('PTN', 'بیمار'), ('CLI', 'کارفرما'), ('CMN', 'مشترک بین همه')], max_length=3, verbose_name='برای')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='BasicInfo.catalogtagspecificationcategory', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'ویژگی (تگ)',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.CreateModel(
            name='CatalogValuedSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('for_who', models.CharField(choices=[('PRS', 'پرسنل'), ('PTN', 'بیمار'), ('CLI', 'کارفرما'), ('CMN', 'مشترک بین همه')], max_length=3, verbose_name='برای')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='BasicInfo.catalogvaluedspecificationcategory', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'ویژگی مقداری',
                'verbose_name_plural': 'ویژگی های مقداری',
            },
        ),
    ]