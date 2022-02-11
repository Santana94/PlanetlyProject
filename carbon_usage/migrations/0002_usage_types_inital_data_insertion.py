from django.db import migrations


usage_types = [
    {
        "id": 100,
        "name": "electricity",
        "unit": "kwh",
        "factor": 1.5
    },
    {
        "id": 101,
        "name": "water",
        "unit": "kg",
        "factor": 26.93
    },
    {
        "id": 102,
        "name": "heating",
        "unit": "kwh",
        "factor": 3.892
    },
    {
        "id": 103,
        "name": "heating",
        "unit": "l",
        "factor": 8.57
    },
    {
        "id": 104,
        "name": "heating",
        "unit": "m3",
        "factor": 19.456
    },
]


def create_usage_types(apps, schema_editor):
    UsageTypes = apps.get_model('carbon_usage', 'UsageTypes')
    for usage_type in usage_types:
        UsageTypes.objects.create(**usage_type)


class Migration(migrations.Migration):
    dependencies = [
        ('carbon_usage', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_usage_types),
    ]
