# Generated by Django 4.2.6 on 2023-11-17 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('browse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='browse.game')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='game',
            field=models.ManyToManyField(through='order.CartItem', to='browse.game'),
        ),
    ]