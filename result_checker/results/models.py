from django.db import models
from django.contrib.auth.models import User

class StudentResult(models.Model):
    school = models.ForeignKey(
        "SchoolSettings",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    symbol_number = models.CharField(max_length=20, unique=True, primary_key=True)
    full_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)

    
    # Subject fields (you can modify these based on your Excel structure)
    subject_1 = models.CharField(max_length=100, blank=True)
    marks_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade_1 = models.CharField(max_length=2, blank=True)
    
    subject_2 = models.CharField(max_length=100, blank=True)
    marks_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade_2 = models.CharField(max_length=2, blank=True)
    
    subject_3 = models.CharField(max_length=100, blank=True)
    marks_3 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade_3 = models.CharField(max_length=2, blank=True)
    
    subject_4 = models.CharField(max_length=100, blank=True)
    marks_4 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade_4 = models.CharField(max_length=2, blank=True)
    
    subject_5 = models.CharField(max_length=100, blank=True)
    marks_5 = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade_5 = models.CharField(max_length=2, blank=True)
    
    # Overall results
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_grade = models.CharField(max_length=10, blank=True)
    result_status = models.CharField(max_length=20, default="PASS")  # PASS/FAIL
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.symbol_number} - {self.full_name}"
    
    class Meta:
        ordering = ['symbol_number']


class ExcelUpload(models.Model):
    excel_file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    semester = models.CharField(max_length=50)
    program = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.program} - {self.semester} - {self.uploaded_at.date()}"
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/')  # stores images in MEDIA_ROOT/team/

    # Optional social links
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class SchoolSettings(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    school_name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='school_logo/', blank=True, null=True)
    
    class Meta:
        verbose_name = "School Settings"
        verbose_name_plural = "School Settings"
    
    def __str__(self):
        return self.school_name
    
   
