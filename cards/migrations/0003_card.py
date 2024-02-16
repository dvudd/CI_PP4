# Generated by Django 4.2.10 on 2024-02-16 16:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_deck'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.deck')),
            ],
        ),
    ]
