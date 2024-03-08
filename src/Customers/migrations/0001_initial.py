# Generated by Django 5.0.2 on 2024-03-07 20:12

import common.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("BasicInfo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=50,
                        validators=[common.validators.trim_string],
                        verbose_name="نام",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=50,
                        validators=[common.validators.trim_string],
                        verbose_name="نام خانوادگی",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "مرد"), ("F", "زن")],
                        max_length=1,
                        verbose_name="جنسیت",
                    ),
                ),
                (
                    "national_code",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="کد ملی"
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(blank=True, null=True, verbose_name="تاریخ تولد"),
                ),
            ],
            options={
                "verbose_name": "کارفرما",
                "verbose_name_plural": "کارفرما ها",
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=50,
                        validators=[common.validators.trim_string],
                        verbose_name="نام",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=50,
                        validators=[common.validators.trim_string],
                        verbose_name="نام خانوادگی",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "مرد"), ("F", "زن")],
                        max_length=1,
                        verbose_name="جنسیت",
                    ),
                ),
                (
                    "national_code",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="کد ملی"
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(blank=True, null=True, verbose_name="تاریخ تولد"),
                ),
            ],
            options={
                "verbose_name": "بیمار",
                "verbose_name_plural": "بیمار ها",
            },
        ),
        migrations.CreateModel(
            name="ClientAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "location_text",
                    models.CharField(max_length=250, verbose_name="آدرس"),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Customers.client",
                    ),
                ),
            ],
            options={
                "verbose_name": "آدرس",
                "verbose_name_plural": "آدرس ها",
            },
        ),
        migrations.CreateModel(
            name="ClientPhoneNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number_type",
                    models.CharField(
                        choices=[("N", "شماره تماس عادی"), ("E", "شماره تماس اضطراری")],
                        default="N",
                        max_length=1,
                        verbose_name="نوع شماره",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=11, verbose_name="شماره تلفن همراه"),
                ),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Customers.client",
                        verbose_name="کارفرما",
                    ),
                ),
            ],
            options={
                "verbose_name": "شماره تماس",
                "verbose_name_plural": "شماره های تماس",
            },
        ),
        migrations.CreateModel(
            name="PatientValuedSpecification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=250)),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Customers.patient",
                    ),
                ),
                (
                    "specification",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="BasicInfo.catalogvaluedspecification",
                    ),
                ),
            ],
            options={
                "verbose_name": "ویژگی بیمار",
                "verbose_name_plural": "ویژگی های بیمار",
            },
        ),
    ]