# results/models.py
from django.db import models

class School(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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