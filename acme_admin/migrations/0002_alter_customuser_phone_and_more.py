# Generated by Django 4.1.2 on 2022-10-22 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_group_is_active'),
        ('acme_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(help_text='Provide Phone number or Email address', max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_department',
            field=models.ForeignKey(blank=True, help_text='Assign Department for Users', on_delete=django.db.models.deletion.CASCADE, related_name='user_department', to='acme_admin.department'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_roles',
            field=models.ForeignKey(blank=True, help_text='Assign roles for users', on_delete=django.db.models.deletion.PROTECT, to='auth.group'),
        ),
    ]
