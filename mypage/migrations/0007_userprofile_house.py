# Generated by Django 3.2.22 on 2023-10-28 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0006_alter_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='house',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
