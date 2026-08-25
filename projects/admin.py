from django.contrib import admin
from .models import Category, ContactMessage, Project, ProjectComponent, ProjectImage, ProjectStep, Tag


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectStepInline(admin.TabularInline):
    model = ProjectStep
    extra = 1


class ProjectComponentInline(admin.TabularInline):
    model = ProjectComponent
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'featured', 'project_date', 'created_at']
    list_filter = ['category', 'featured', 'project_date']
    search_fields = ['title', 'description', 'category__name', 'tags__name']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    inlines = [ProjectImageInline, ProjectStepInline, ProjectComponentInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.site_header = 'Circuit Nest Administration'
admin.site.site_title = 'Circuit Nest Admin'