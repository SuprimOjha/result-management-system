# results/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField

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


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(help_text="Short summary of the blog post (150-200 characters)")
    content = HTMLField(help_text="Write your blog content here")
    featured_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    # SEO Meta fields
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=200, blank=True, help_text="comma-separated keywords")
    
    # Publishing control
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Mark as featured blog")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Views tracking
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def read_time(self):
        """Calculate estimated reading time in minutes"""
        word_count = len(self.content.split())
        reading_time = max(1, word_count // 200)  # Assuming 200 words per minute
        return f"{reading_time} min read"