from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    project_date = models.DateField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='projects/images/', blank=True, null=True)
    video = models.FileField(upload_to='projects/videos/', blank=True, null=True, validators=[FileExtensionValidator(['mp4', 'webm', 'mov'])])
    github_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-project_date', '-created_at']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class ProjectStep(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['step_number', 'id']


class ProjectComponent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='components')
    component_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.component_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'