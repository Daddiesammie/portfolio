from django.contrib import admin
from .models import (
    Profile, Education, Experience, TechnicalSkill,
    Language, Project, Certification, Award, Reference
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'phone')
    search_fields = ('full_name', 'email')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'field', 'start_date', 'end_date')
    list_filter = ('education_type', 'end_date')
    search_fields = ('school', 'degree', 'field')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'location', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('company', 'position')

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'years_of_experience')
    list_filter = ('category', 'proficiency')
    search_fields = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency')
    list_filter = ('proficiency',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'technologies')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'date_obtained', 'expiry_date')
    list_filter = ('date_obtained', 'issuer')
    search_fields = ('name', 'issuer')

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'date_received')
    list_filter = ('date_received',)
    search_fields = ('title', 'issuer')

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'company', 'email')
    search_fields = ('name', 'company')
