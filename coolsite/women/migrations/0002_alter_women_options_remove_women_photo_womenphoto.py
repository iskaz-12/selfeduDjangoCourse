# Generated by Django 4.2.4 on 2023-08-24 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='women',
            options={'verbose_name': 'Известные женщины', 'verbose_name_plural': 'Известные женщины'},
        ),
        migrations.RemoveField(
            model_name='women',
            name='photo',
        ),
        migrations.CreateModel(
            name='WomenPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('women', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='women.women', verbose_name='Известные женщины')),
            ],
        ),
    ]
