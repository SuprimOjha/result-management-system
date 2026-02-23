from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("results", "0004_teammember"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="schoolsettings",
            name="owner",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="schoolsettings",
            name="address",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="schoolsettings",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="school_logo/"),
        ),
        migrations.AlterField(
            model_name="schoolsettings",
            name="phone",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
