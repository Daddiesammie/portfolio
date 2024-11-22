from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at', 'tags')
    search_fields = ('title', 'description')
    inlines = [ProjectImageInline]

admin.site.register(ProjectImage)