from django.contrib import admin
from .models import SchoolSettings, StudentResult, ExcelUpload, TeamMember

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('symbol_number', 'full_name', 'program', 'semester', 'percentage', 'result_status')
    list_filter = ('program', 'semester', 'result_status')
    search_fields = ('symbol_number', 'full_name')
    list_per_page = 20

@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    list_display = ('program', 'semester', 'uploaded_at', 'excel_file')
    list_filter = ('program', 'semester')
    date_hierarchy = 'uploaded_at'

admin.site.register(SchoolSettings)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
