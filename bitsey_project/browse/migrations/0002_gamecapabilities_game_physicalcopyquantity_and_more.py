# Generated by Django 4.2.6 on 2023-11-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameCapabilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='physicalCopyQuantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='gameCapabilities',
            field=models.ManyToManyField(to='browse.gamecapabilities'),
        ),
    ]
