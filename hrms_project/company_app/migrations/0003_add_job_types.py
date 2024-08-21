from django.db import migrations

def add_job_types(apps, schema_editor):
    JobType = apps.get_model('company_app', 'JobType')
    JobType.objects.bulk_create([
        JobType(name='Full-Time'),
        JobType(name='Part-Time'),
        JobType(name='Contract'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0001_initial'),  # Replace with the actual previous migration file name
    ]

    operations = [
        migrations.RunPython(add_job_types),
    ]
