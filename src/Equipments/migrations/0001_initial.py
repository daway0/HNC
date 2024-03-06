# Generated by Django 5.0.2 on 2024-03-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('current_price', models.IntegerField(default=0, verbose_name='قیمت فعلی')),
            ],
            options={
                'verbose_name': 'تجهیز',
                'verbose_name_plural': 'تجهیزات',
            },
        ),
    ]
