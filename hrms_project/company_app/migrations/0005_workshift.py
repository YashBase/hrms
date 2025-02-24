# Generated by Django 5.1 on 2024-08-20 17:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0004_merge_0002_jobtype_salaryinfo_0003_add_job_types'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_type', models.CharField(choices=[('Day Shift', 'Day Shift'), ('Night Shift', 'Night Shift'), ('Evening Shift', 'Evening Shift')], max_length=20)),
                ('total_work_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
