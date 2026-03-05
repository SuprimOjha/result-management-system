# results/models.py
from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ensure a unique code exists before saving
        if not self.code:
            # simple default code based on name
            base = ''.join(ch for ch in self.name if ch.isalnum()).upper()[:4]
            if not base:
                base = 'SCH'
            code = base
            import random, string
            # try to find unique code
            while School.objects.filter(code=code).exists():
                suffix = ''.join(random.choices(string.digits, k=2))
                code = f"{base}{suffix}"
            self.code = code
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.school.name if self.school else 'No School'}"

class Result(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=50)
    symbol_number = models.CharField(max_length=12)
    semester = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=50)
    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    department = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    status = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} ({self.symbol_number})"