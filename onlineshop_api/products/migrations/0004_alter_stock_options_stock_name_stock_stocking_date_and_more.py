# Generated by Django 5.1.2 on 2024-10-29 09:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image_stock_stockmovement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['-stocking_date'], 'verbose_name': 'Stock', 'verbose_name_plural': 'Stocks'},
        ),
        migrations.AddField(
            model_name='stock',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='stocking_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='products.product'),
        ),
    ]
