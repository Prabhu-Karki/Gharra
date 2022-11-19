# Generated by Django 4.0.6 on 2022-11-18 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainsite', '0002_remove_customer_zipcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('color', models.CharField(blank=True, default='Black', max_length=30)),
                ('storage', models.PositiveIntegerField(default=64)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.product')),
            ],
        ),
    ]