# results/admin.py
from django.contrib import admin
from .models import School, Result, Blog, BlogCategory

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'symbol_number', 'school', 'semester', 'exam_type', 'obtained_marks', 'total_marks', 'status')
    search_fields = ('student_name', 'symbol_number', 'roll_number')
    list_filter = ('school', 'semester', 'exam_type', 'status')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'featured', 'views', 'created_at')
    list_filter = ('is_published', 'featured', 'category', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'views')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Meta Information', {
            'fields': ('category', 'author', 'meta_description', 'meta_keywords')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new blog
            obj.author = request.user
        super().save_model(request, obj, form, change)