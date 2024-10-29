# Generated by Django 5.1.2 on 2024-10-29 08:29

import django.db.models.deletion
import django.utils.timezone
import shared.utils.generate_file_upload_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=shared.utils.generate_file_upload_path.generate_file_upload_path),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('movement_type', models.CharField(choices=[('IN', 'Stock In'), ('OUT', 'Stock Out')], max_length=3)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='products.stock')),
            ],
            options={
                'verbose_name': 'Stock Movement',
                'verbose_name_plural': 'Stock Movements',
                'ordering': ['-created_at'],
            },
        ),
    ]
