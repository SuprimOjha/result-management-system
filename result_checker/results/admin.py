# results/admin.py
from django.contrib import admin
from .models import School, Result

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'symbol_number', 'school', 'semester', 'exam_type', 'obtained_marks', 'total_marks', 'status')
    search_fields = ('student_name', 'symbol_number', 'roll_number')
    list_filter = ('school', 'semester', 'exam_type', 'status')