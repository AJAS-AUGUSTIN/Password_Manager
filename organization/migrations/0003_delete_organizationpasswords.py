# Generated by Django 4.0.4 on 2022-04-20 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_addorganizationpasswords_organizationpasswords'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrganizationPasswords',
        ),
    ]
